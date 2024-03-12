from django.views import generic # ジェネリックビュー
from django.urls import reverse_lazy
from django.contrib import messages # システムメッセージ
from django.shortcuts import redirect
import numpy as np # グラフ
import pandas as pd # グラフ
from django_pandas.io import read_frame # グラフ

from .models import Payment, PaymentCategory, Income, IncomeCategory
from .forms import PaymentSearchForm, IncomeSearchForm,\
                    PaymentCreateForm, IncomeCreateForm,\
                    TransitionGraphSearchForm
from .plugin_plotly import GraphGenerator # グラフ

# 支出一覧
class PaymentList(generic.ListView):
    template_name = 'kakeibo/payment_list.html' # レンダリングするテンプレート
    model = Payment # Paymentモデルのレコードを渡す {{payment_list}}もしくは{{object_list}}
    ordering = '-date'

    def get_queryset(self):
        queryset = super().get_queryset() # PaymentList.objects.all()と同等
        self.form = form = PaymentSearchForm(self.request.GET or None)

        if form.is_valid(): # バリデーションチェック
            # form.cleaned_data：バリデーションをクリアしたデータのみをディクショナリに格納
            year = form.cleaned_data.get('year') # 'year'キーで値を取り出す

            # 選択なし：文字列'0'が入るため除外
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            # 選択なし：文字列'0'が入るため除外
            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

            # 〇〇円以上の絞り込み
            greater_than = form.cleaned_data.get('greater_than')
            if greater_than:
                queryset = queryset.filter(price__gte=greater_than)

            # 〇〇円以下の絞り込み
            less_than = form.cleaned_data.get('less_than')
            if less_than:
                queryset = queryset.filter(price__lte=less_than)

            # キーワードの絞り込み
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                # 空欄で区切り、順番に絞る、and検索
                if key_word:
                    for word in key_word.split():
                        queryset = queryset.filter(description__icontains=word)

            # カテゴリで絞り込み
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs): # オーバーライド
        context = super().get_context_data(**kwargs)  # 親クラスの get_context_dataメソッドを実行
        context['search_form'] = self.form  # search_form変数をcontextに追加

        return context # テンプレートをcontextに渡す{{ search_form }}で使用

# 収入一覧
class IncomeList(generic.ListView):
    template_name = 'kakeibo/income_list.html'
    model = Income
    ordering = '-date'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = IncomeSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        return context

# 支出登録
class PaymentCreate(generic.CreateView):
    template_name = 'kakeibo/register.html'
    model = Payment
    form_class = PaymentCreateForm

    def get_context_data(self, **kwargs): #オーバーライド
        context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = '支出登録' # contextに追加
        return context

    def get_success_url(self):
        return reverse_lazy('kakeibo:payment_list')

    def form_valid(self, form):
        self.object = payment = form.save()
        messages.info(self.request,
                        f'支出を登録しました\n'
                        f'日付:{payment.date}\n'
                        f'カテゴリ:{payment.category}\n'
                        f'金額:{payment.price}円')
        return redirect(self.get_success_url())

# 収入登録
class IncomeCreate(generic.CreateView):
    template_name = 'kakeibo/register.html'
    model = Income
    form_class = IncomeCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入登録'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeibo:income_list')

    def form_valid(self, form):
        self.object = income = form.save()
        messages.info(self.request,
                        f'収入を登録しました\n'
                        f'日付:{income.date}\n'
                        f'カテゴリ:{income.category}\n'
                        f'金額:{income.price}円')
        return redirect(self.get_success_url())

# 支出更新
class PaymentUpdate(generic.UpdateView):
    template_name = 'kakeibo/register.html'
    model = Payment
    form_class = PaymentCreateForm

    def get_context_data(self, **kwargs): # オーバーライド
        context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = '支出更新' # contextに追加
        return context

    def get_success_url(self):
        return reverse_lazy('kakeibo:payment_list')

    def form_valid(self, form):
        self.object = payment = form.save()
        messages.info(self.request,
                        f'支出を更新しました\n'
                        f'日付:{payment.date}\n'
                        f'カテゴリ:{payment.category}\n'
                        f'金額:{payment.price}円')
        return redirect(self.get_success_url())

# 収入更新
class IncomeUpdate(generic.UpdateView):
    template_name = 'kakeibo/register.html'
    model = Income
    form_class = IncomeCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入更新'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeibo:income_list')

    def form_valid(self, form):
        self.object = income = form.save()
        messages.info(self.request,
                        f'収入を更新しました\n'
                        f'日付:{income.date}\n'
                        f'カテゴリ:{income.category}\n'
                        f'金額:{income.price}円')
        return redirect(self.get_success_url())

# 支出削除
class PaymentDelete(generic.DeleteView):
    template_name = 'kakeibo/delete.html'
    model = Payment

    def get_success_url(self):
        return reverse_lazy('kakeibo:payment_list')

    def get_context_data(self, **kwargs): # オーバーライド
        context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = '支出削除確認' # contextに追加

        return context

    def delete(self, request, *args, **kwargs):
        self.object = payment = self.get_object()

        payment.delete()
        messages.info(self.request,
                        f'支出を削除しました\n'
                        f'日付:{payment.date}\n'
                        f'カテゴリ:{payment.category}\n'
                        f'金額:{payment.price}円')
        return redirect(self.get_success_url())

# 収入削除
class IncomeDelete(generic.DeleteView):
    template_name = 'kakeibo/delete.html'
    model = Income

    def get_success_url(self):
        return reverse_lazy('kakeibo:income_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入削除確認'

        return context

    def delete(self, request, *args, **kwargs):
        self.object = income = self.get_object()
        income.delete()
        messages.info(self.request,
                        f'収入を削除しました\n'
                        f'日付:{income.date}\n'
                        f'カテゴリ:{income.category}\n'
                        f'金額:{income.price}円')
        return redirect(self.get_success_url())

# 月間支出ダッシュボード
class MonthDashboard(generic.TemplateView):
    template_name = 'kakeibo/month_dashboard.html'

    def get_context_data(self, **kwargs): # オーバーライド
        context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行

        # これから表示する年月
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        context['year_month'] = f'{year}年{month}月' # contextに追加

        # 前月と次月をcontextに追加
        if month == 1:
            prev_year = year - 1
            prev_month = 12
        else:
            prev_year = year
            prev_month = month - 1

        if month == 12:
            next_year = year + 1
            next_month = 1
        else:
            next_year = year
            next_month = month + 1
        context['prev_year'] = prev_year   # contextに追加
        context['prev_month'] = prev_month
        context['next_year'] = next_year
        context['next_month'] = next_month

        # PaymentモデルのQuerySetを取り出す
        queryset = Payment.objects.filter(date__year=year)
        queryset = queryset.filter(date__month=month)
        # 後の工程のエラー対策
        if not queryset:
            return context # QuerySetが何もない時はcontextを返す

        # 取り出したQuerySetをpandasデータフレーム(df)化
        df = read_frame(queryset,
                        fieldnames=['date', 'price', 'category'])
        # plugin_plotly.pyのクラスでインスタンスを作成
        gen = GraphGenerator()

        # pieチャートの素材
        # カテゴリー毎に金額をpivot集計
        df_pie = pd.pivot_table(df, index='category', values='price', aggfunc=np.sum)
        # カテゴリー情報をdf_pie.index.valuesで取り出してリスト化
        pie_labels = list(df_pie.index.values)
        # 金額情報をdf_pie.valuesで取り出してディクショナリ化
        pie_values = [val[0] for val in df_pie.values]
        plot_pie = gen.month_pie(labels=pie_labels, values=pie_values) # genインスタンスmonth_pieメソッド
        context['plot_pie'] = plot_pie # contextに追加

        # テーブルでのカテゴリと集計金額の表示
        # ディクショナリ{カテゴリ:集計金額, カテゴリ:集計金額…}をcontextに追加
        context['table_set'] = df_pie.to_dict()['price']
        # totalの数字を計算してcontextに追加
        context['total_payment'] = df['price'].sum()

        # 日別棒グラフの素材
        df_bar = pd.pivot_table(df, index='date', values='price', aggfunc=np.sum) # 日付ごとに金額をピボット集計
        dates = list(df_bar.index.values) # 日付情報をリスト化
        heights = [val[0] for val in df_bar.values] # 金額情報をディクショナリ化
        plot_bar = gen.month_daily_bar(x_list=dates, y_list=heights)
        context['plot_bar'] = plot_bar

        return context

# # 月毎の収支推移：絞り込み機能なし
# class TransitionView(generic.TemplateView):
#     template_name = 'kakeibo/transition.html'

#     def get_context_data(self, **kwargs): # オーバーライド
#         context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
#         payment_queryset = Payment.objects.all()
#         income_queryset = Income.objects.all()
#         # データフレーム(df)化
#         payment_df = read_frame(payment_queryset,
#                                 fieldnames=['date', 'price'])
#         # 日付カラムをdatetime化して、Y-m表記に変換
#         payment_df['date'] = pd.to_datetime(payment_df['date'])
#         payment_df['month'] = payment_df['date'].dt.strftime('%Y-%m')
#         # monthカラムでpivot集計
#         payment_df = pd.pivot_table(payment_df, index='month', values='price', aggfunc=np.sum)
#         # x軸
#         months_payment = list(payment_df.index.values)
#         # y軸
#         payments = [y[0] for y in payment_df.values]

#         # 収入も同様
#         income_df = read_frame(income_queryset,
#                                 fieldnames=['date', 'price'])
#         income_df['date'] = pd.to_datetime(income_df['date'])
#         income_df['month'] = income_df['date'].dt.strftime('%Y-%m')
#         income_df = pd.pivot_table(income_df, index='month', values='price', aggfunc=np.sum)
#         months_income = list(income_df.index.values)
#         incomes = [y[0] for y in income_df.values]

#         # plugin_plotly.pyのクラスでインスタンスを生成
#         gen = GraphGenerator()
#         context['transition_plot'] = gen.transition_plot(
#                                         x_list_payment=months_payment,
#                                         y_list_payment=payments,
#                                         x_list_income=months_income,
#                                         y_list_income=incomes
#                                         )
#         return context


# 月毎の収支推移：絞り込み機能付き
# 支出のみ、収入のみのグラフを表示
# 支出、収入それぞれにおいてカテゴリを単一で表示
# 検索実行⇒クエリを絞り込みデータフレーム化⇒グラフ生成
class TransitionView(generic.TemplateView):

    template_name = 'kakeibo/transition.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_queryset = Payment.objects.all()
        income_queryset = Income.objects.all()
        self.form = form = TransitionGraphSearchForm(self.request.GET or None)
        context['search_form'] = self.form

        graph_visible = None
        # 表示の切り替えでplotlyに渡すデータ
        months_payment = None
        payments = None
        months_income = None
        incomes = None

        if form.is_valid(): # バリデーションチェック
            # 支出カテゴリーで絞り込む
            payment_category = form.cleaned_data.get('payment_category')
            if payment_category:
                payment_queryset = payment_queryset.filter(category=payment_category)
            # 収入カテゴリーで絞り込む
            income_category = form.cleaned_data.get('income_category')
            if income_category:
                income_queryset = income_queryset.filter(category=income_category)
            # 表示グラフ
            graph_visible = form.cleaned_data.get('graph_visible')

        # グラフ表示指定がない、もしくは支出グラフ表示を選択
        if not graph_visible or graph_visible == 'Payment':
            payment_df = read_frame(payment_queryset,
                                    fieldnames=['date', 'price'])
            payment_df['date'] = pd.to_datetime(payment_df['date'])
            payment_df['month'] = payment_df['date'].dt.strftime('%Y-%m')
            payment_df = pd.pivot_table(
                                        payment_df,
                                        index='month',
                                        values='price',
                                        aggfunc=np.sum
                                        )
            months_payment = list(payment_df.index.values)
            payments = [y[0] for y in payment_df.values]

        # グラフ表示指定がない、もしくは収入グラフ表示を選択
        if not graph_visible or graph_visible == 'Income':
            income_df = read_frame(income_queryset,
                                    fieldnames=['date', 'price'])
            income_df['date'] = pd.to_datetime(income_df['date'])
            income_df['month'] = income_df['date'].dt.strftime('%Y-%m')
            income_df = pd.pivot_table(
                                        income_df,
                                        index='month',
                                        values='price',
                                        aggfunc=np.sum
                                        )
            months_income = list(income_df.index.values)
            incomes = [y[0] for y in income_df.values]

        # plugin_plotly.pyのクラスでインスタンスを生成
        gen = GraphGenerator()
        # if条件分岐（表示グラフ選択）により書換えられた値 または None が入った
        # months_payment、payments、months_income、incomes
        # を引数として渡し、グラフを作成する（Noneが渡されたグラフは作成されない）
        context['transition_plot'] = gen.transition_plot(
                                        x_list_payment=months_payment,
                                        y_list_payment=payments,
                                        x_list_income=months_income,
                                        y_list_income=incomes
                                        )

        return context
