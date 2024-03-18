from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages # システムメッセージ
from django.contrib.auth.mixins import LoginRequiredMixin # ログインユーザーのみ閲覧可能
import numpy as np # グラフ
import pandas as pd # グラフ
from django_pandas.io import read_frame # グラフ

from .models import Payment, PaymentCategory, Income, IncomeCategory
from .forms import PaymentSearchForm, IncomeSearchForm \
                    , PaymentCreateForm, IncomeCreateForm \
                    # , TransitionGraphSearchForm
from .plugin_plotly import GraphGenerator # グラフ

# 支出一覧
class PaymentList(LoginRequiredMixin, generic.ListView):
    # template_name = 'money/payment_list.html'
    template_name = 'money/list.html'
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

            # ユーザーで絞り込み
            account_id = form.cleaned_data.get('account_id')
            if account_id:
                queryset = queryset.filter(account_id=account_id)

        return queryset

    def get_context_data(self, **kwargs): # オーバーライド
        context = super().get_context_data(**kwargs)  # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = '支出一覧' # list.html
        context['search_form'] = self.form  # search_form変数をcontextに追加
        context['lists'] = self.get_queryset() # list.html
        # context['payment_list'] = self.get_queryset()  # 不要payment_list.html

        return context # テンプレートをcontextに渡す{{ search_form }}で使用


# 収入一覧
class IncomeList(LoginRequiredMixin, generic.ListView):
    # template_name = 'money/income_list.html'
    template_name = 'money/list.html'

    model = Income
    ordering = '-date'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = IncomeSearchForm(self.request.GET or None)

        if form.is_valid():
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

            # ユーザーで絞り込み
            account_id = form.cleaned_data.get('account_id')
            if account_id:
                queryset = queryset.filter(account_id=account_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入一覧'  # list.html
        context['search_form'] = self.form
        context['lists'] = self.get_queryset() # list.html
        # context['income_list'] = self.get_queryset()  # 不要imcome_list.html
        return context

# 支出登録
class PaymentCreate(LoginRequiredMixin, generic.CreateView):
    template_name = 'money/create.html'
    model = Payment
    form_class = PaymentCreateForm

    def get_context_data(self, **kwargs): #オーバーライド
        context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = '支出登録' # contextに追加
        return context

    def get_success_url(self):
        return reverse_lazy('money:payment_list')

    def form_valid(self, form):
        self.object = payment = form.save()
        messages.info(self.request,
                        f'支出を登録しました\n'
                        f'日付:{payment.date}\n'
                        f'カテゴリ:{payment.category}\n'
                        f'金額:{payment.price}円')
        return redirect(self.get_success_url())

# 収入登録
class IncomeCreate(LoginRequiredMixin, generic.CreateView):
    template_name = 'money/create.html'
    model = Income
    form_class = IncomeCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入登録'
        return context

    def get_success_url(self):
        return reverse_lazy('money:income_list')

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
    template_name = 'money/create.html'
    model = Payment
    form_class = PaymentCreateForm

    def get_context_data(self, **kwargs): # オーバーライド
        context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = '支出更新' # contextに追加
        return context

    def get_success_url(self):
        return reverse_lazy('money:payment_list')

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
    template_name = 'money/create.html'
    model = Income
    form_class = IncomeCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入更新'
        return context

    def get_success_url(self):
        return reverse_lazy('money:income_list')

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
    template_name = 'money/delete.html'
    model = Payment

    def get_success_url(self):
        return reverse_lazy('money:payment_list')

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
    template_name = 'money/delete.html'
    model = Income

    def get_success_url(self):
        return reverse_lazy('money:income_list')

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


# # 月間ダッシュボード
# class MonthDashboard(generic.TemplateView):
#     template_name = 'money/month_dashboard.html'

#     def get_context_data(self, **kwargs): # オーバーライド
#         context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行

#         # これから表示する年月
#         year = int(self.kwargs.get('year'))
#         month = int(self.kwargs.get('month'))
#         context['year_month'] = f'{year}年{month}月' # contextに追加

#         # 前月と次月をcontextに追加
#         if month == 1:
#             prev_year = year - 1
#             prev_month = 12
#         else:
#             prev_year = year
#             prev_month = month - 1

#         if month == 12:
#             next_year = year + 1
#             next_month = 1
#         else:
#             next_year = year
#             next_month = month + 1
#         context['prev_year'] = prev_year   # contextに追加
#         context['prev_month'] = prev_month
#         context['next_year'] = next_year
#         context['next_month'] = next_month

#         # PaymentモデルのQuerySetを取り出す
#         queryset = Payment.objects.filter(date__year=year)
#         queryset = queryset.filter(date__month=month)
#         # 後の工程のエラー対策
#         if not queryset:
#             return context # QuerySetが何もない時はcontextを返す
#         # 取り出したQuerySetをpandasデータフレーム(df)化
#         df = read_frame(queryset,
#                         fieldnames=['date', 'price', 'category'])
#         # plugin_plotly.pyのGraphGeneratorクラスでインスタンス作成
#         gen = GraphGenerator()
#         # pieチャートの素材作成
#         # カテゴリー毎に金額をpivot集計
#         df_pie = pd.pivot_table(df, index='category', values='price', aggfunc=np.sum)
#         # カテゴリー情報をdf_pie.index.valuesで取り出してリスト化
#         pie_labels = list(df_pie.index.values)
#         # 金額情報をdf_pie.valuesで取り出してディクショナリ化
#         pie_values = [val[0] for val in df_pie.values]
#         plot_pie = gen.month_pie(labels=pie_labels, values=pie_values) # genインスタンスmonth_pieメソッド
#         context['payment_pie'] = plot_pie # contextに追加

#         # テーブルでのカテゴリと集計金額の表示
#         # ディクショナリ{カテゴリ:集計金額, カテゴリ:集計金額…}をcontextに追加
#         context['payment_table_set'] = df_pie.to_dict()['price']
#         # totalの数字を計算してcontextに追加
#         context['total_payment'] = df['price'].sum()

#         # 日別棒グラフの素材
#         df_bar = pd.pivot_table(df, index='date', values='price', aggfunc=np.sum) # 日付ごとに金額をピボット集計
#         dates = list(df_bar.index.values) # 日付情報をリスト化
#         heights = [val[0] for val in df_bar.values] # 金額情報をディクショナリ化
#         plot_bar = gen.month_daily_bar(x_list=dates, y_list=heights)
#         context['payment_bar'] = plot_bar

#         return context

# 月間支出・収入ダッシュボード
class MonthDashboard(generic.TemplateView):
    template_name = 'money/month_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        context['year_month'] = f'{year}年{month}月'

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
        context['prev_year'] = prev_year
        context['prev_month'] = prev_month
        context['next_year'] = next_year
        context['next_month'] = next_month

        # PaymentモデルのQuerySetを取り出す
        payment_queryset = Payment.objects.filter(date__year=year)
        payment_queryset = payment_queryset.filter(date__month=month)
        # 後の工程のエラー対策
        if not payment_queryset:
            return context
        # 取り出したQuerySetをpandasデータフレーム(df)化
        payment_df = read_frame(payment_queryset, fieldnames=['date', 'price', 'category'])

        # IncomeモデルのQuerySetを取り出す
        income_queryset = Income.objects.filter(date__year=year)
        income_queryset = income_queryset.filter(date__month=month)
        if not income_queryset:
            return context
        income_df = read_frame(income_queryset, fieldnames=['date', 'price', 'category'])

        # plugin_plotly.pyのGraphGeneratorクラスでインスタンス作成
        gen = GraphGenerator()

        # Paymentデータに基づくグラフ
        payment_pie_labels, payment_pie_values = self.prepare_data(payment_df)
        payment_pie = gen.month_pie(labels=payment_pie_labels, values=payment_pie_values)
        context['payment_pie'] = payment_pie
        # カテゴリー毎に金額をpivot集計
        payment_table_set = pd.pivot_table(payment_df, index='category', values='price', aggfunc=np.sum)
        # テーブルでのカテゴリと集計金額の表示
        # ディクショナリ{カテゴリ:集計金額, カテゴリ:集計金額…}をcontextに追加
        context['payment_table_set'] = payment_table_set.to_dict()['price']
        # totalの数字を計算してcontextに追加
        context['total_payment'] = payment_df['price'].sum()
        # 日別棒グラフ
        payment_bar_dates, payment_bar_heights = self.prepare_data(payment_df, by='date')
        payment_bar = gen.month_daily_bar(x_list=payment_bar_dates, y_list=payment_bar_heights)
        context['payment_bar'] = payment_bar

        # Incomeデータに基づくグラフ
        income_pie_labels, income_pie_values = self.prepare_data(income_df)
        income_pie = gen.month_pie(labels=income_pie_labels, values=income_pie_values)
        context['income_pie'] = income_pie

        income_table_set = pd.pivot_table(income_df, index='category', values='price', aggfunc=np.sum)
        context['income_table_set'] = income_table_set.to_dict()['price']
        context['total_income'] = income_df['price'].sum()

        income_bar_dates, income_bar_heights = self.prepare_data(income_df, by='date')
        income_bar = gen.month_daily_bar_income(x_list=income_bar_dates, y_list=income_bar_heights)
        context['income_bar'] = income_bar

        return context

    def prepare_data(self, df, by='category'):
        if by == 'category':
            pivot_df = pd.pivot_table(df, index=by, values='price', aggfunc=np.sum)
            labels = list(pivot_df.index.values)
            values = [val[0] for val in pivot_df.values]
            return labels, values
        elif by == 'date':
            pivot_df = pd.pivot_table(df, index='date', values='price', aggfunc=np.sum)
            dates = list(pivot_df.index.values)
            heights = [val[0] for val in pivot_df.values]
            return dates, heights
