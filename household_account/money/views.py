from django.views.generic import ListView, CreateView, UpdateView \
                                , DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages # システムメッセージ
from django.contrib.auth.mixins import LoginRequiredMixin # ログインユーザーのみ閲覧可能
import numpy as np # グラフ
import pandas as pd # グラフ
from django_pandas.io import read_frame # グラフ
from django.contrib.auth import get_user_model # 設定されたユーザーモデルのインポート
from django.db.models import Q

from .models import Payment, PaymentCategory, Income, IncomeCategory \
                    ,PaymentItem, IncomeItem, PaymentOrigItem, IncomeOrigItem
from .forms import PaymentSearchForm, IncomeSearchForm \
                    , PaymentCreateForm, IncomeCreateForm \
                    , PaymentOrigItemForm, IncomeOrigItemForm
from .plugin_plotly import GraphGenerator # グラフ

# 支出一覧
class PaymentList(LoginRequiredMixin, ListView):
    template_name = 'money/list.html'
    model = Payment
    ordering = '-date'
    paginate_by = 5  # ページごとに表示するアイテムの数

    def get_queryset(self):
        login_user = self.request.user  # ログイン中のユーザーを取得
        queryset = super().get_queryset() # PaymentList.objects.all()と同等
        queryset = queryset.filter(account_id=login_user)
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

            # カテゴリで絞り込み
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)

            # キーワードの絞り込み
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                # スペース区切り検索（項目、ユーザー設定項目、備考から検索）
                if key_word:
                    for word in key_word.split():
                        queryset = queryset.filter(
                                Q(description__icontains=word)
                                |Q(item__name__icontains=word)
                                |Q(user_item__name__icontains=word))
        return queryset

    def get_context_data(self, **kwargs): # オーバーライド
        context = super().get_context_data(**kwargs)  # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = '支出一覧' # list.htmlで使用
        context['search_form'] = self.form  # search_form変数をcontextに追加
        return context # テンプレートへcontextを渡す


# 収入一覧
class IncomeList(LoginRequiredMixin, ListView):
    template_name = 'money/list.html'
    model = Income
    ordering = '-date'
    paginate_by = 5

    def get_queryset(self):
        login_user = self.request.user  # ログイン中のユーザーを取得
        queryset = super().get_queryset()
        queryset = queryset.filter(account_id=login_user)
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

            # カテゴリで絞り込み
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)

            # キーワードの絞り込み
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                # スペース区切り検索（項目、ユーザー設定項目、備考から検索）
                if key_word:
                    for word in key_word.split():
                        queryset = queryset.filter(
                                Q(description__icontains=word)
                                |Q(item__name__icontains=word)
                                |Q(user_item__name__icontains=word))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入一覧'  # list.htmlで使用
        context['search_form'] = self.form
        return context

class PaymentCreate(LoginRequiredMixin, CreateView):
    template_name = 'money/create.html'
    model = Payment
    form_class = PaymentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '支出登録'
        return context

    def get_success_url(self):
        return reverse_lazy('money:payment_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # ログイン中のユーザーを渡す
        return kwargs

    def form_valid(self, form):
        login_user = self.request.user
        self.object = payment = form.save(commit=False)
        payment.account_id = login_user
        payment.save()
        messages.info(self.request,
                        f'支出を登録しました。\n'
                        f'日付：{payment.date}\n'
                        f'カテゴリ：{payment.category}\n'
                        f'金額：{payment.price}円')
        return redirect(self.get_success_url())

# 収入登録
class IncomeCreate(LoginRequiredMixin, CreateView):
    template_name = 'money/create.html'
    model = Income
    form_class = IncomeCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入登録'
        return context

    def get_success_url(self):
        return reverse_lazy('money:income_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # ログイン中のユーザーを渡す
        return kwargs

    def form_valid(self, form):
        # self.object = income = form.save()
        login_user = self.request.user  # ログイン中のユーザーを取得
        self.object = income = form.save(commit=False)
        income.account_id = login_user
        income.save()
        messages.info(self.request,
                        f'収入を登録しました。\n'
                        f'日付：{income.date}\n'
                        f'カテゴリ：{income.category}\n'
                        f'金額：{income.price}円')
        return redirect(self.get_success_url())

# ユーザー設定支出項目登録
class PaymentOrigItemRegister(LoginRequiredMixin, CreateView):
    template_name = "money/item_register.html"
    model = PaymentOrigItem
    form_class = PaymentOrigItemForm   # 登録用フォームを設定

    def get_queryset(self):
        login_user = self.request.user  # ログイン中のユーザーを取得
        queryset = super().get_queryset() # PaymentList.objects.all()と同等
        queryset = queryset.filter(account_id=login_user)
        self.form = PaymentOrigItemForm(self.request.GET or None)
        return queryset

    def get_context_data(self, **kwargs): #オーバーライド
        context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = 'ユーザー設定支出項目登録'
        context['lists'] = self.get_queryset()
        return context

    def get_success_url(self):
        return reverse_lazy('money:payment_create')

    def form_valid(self, form):
        login_user = self.request.user  # ログイン中のユーザーを取得
        self.object = payment = form.save(commit=False)
        payment.account_id = login_user
        payment.save()
        return redirect(self.get_success_url())

# ユーザー設定収入項目登録
class IncomeOrigItemRegister(LoginRequiredMixin, CreateView):
    template_name = "money/item_register.html"
    model = IncomeOrigItem
    form_class = IncomeOrigItemForm   # 登録用フォームを設定

    def get_queryset(self):
        login_user = self.request.user  # ログイン中のユーザーを取得
        queryset = super().get_queryset() # PaymentList.objects.all()と同等
        queryset = queryset.filter(account_id=login_user)
        self.form = IncomeOrigItemForm(self.request.GET or None)
        return queryset

    def get_context_data(self, **kwargs): #オーバーライド
        context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = 'ユーザー設定収入項目登録'
        context['lists'] = self.get_queryset()
        return context

    def get_success_url(self):
        return reverse_lazy('money:income_create')

    def form_valid(self, form):
        login_user = self.request.user  # ログイン中のユーザーを取得
        self.object = income = form.save(commit=False)
        income.account_id = login_user
        income.save()
        return redirect(self.get_success_url())

# 支出更新
class PaymentUpdate(LoginRequiredMixin, UpdateView):
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
                        f'支出を更新しました。\n'
                        f'日付：{payment.date}\n'
                        f'カテゴリ：{payment.category}\n'
                        f'金額：{payment.price}円')
        return redirect(self.get_success_url())

# 収入更新
class IncomeUpdate(LoginRequiredMixin, UpdateView):
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
                        f'収入を更新しました。\n'
                        f'日付：{income.date}\n'
                        f'カテゴリ：{income.category}\n'
                        f'金額：{income.price}円')
        return redirect(self.get_success_url())

# 支出削除
class PaymentDelete(LoginRequiredMixin, DeleteView):
    template_name = 'money/delete.html'
    model = Payment

    def get_context_data(self, **kwargs): # オーバーライド
        context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = '支出削除' # contextに追加
        return context

    # def deleteで作成するとメッセージが表示されないためdef postに変更
    def post(self, request, *args, **kwargs):
        self.object = payment = self.get_object()
        payment.delete()
        messages.info(request,
                        f'支出を削除しました。\n'
                        f'日付：{payment.date}\n'
                        f'カテゴリ：{payment.category}\n'
                        f'金額：{payment.price}円')
        return redirect(reverse_lazy('money:payment_list'))

# 収入削除
class IncomeDelete(LoginRequiredMixin, DeleteView):
    template_name = 'money/delete.html'
    model = Income

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入削除'
        return context

    def get_success_url(self):
        return reverse_lazy('money:income_list')

    # def deleteで作成するとメッセージが表示されないためdef postに変更
    def post(self, request, *args, **kwargs):
        self.object = income = self.get_object()
        income.delete()
        messages.info(self.request,
                        f'収入を削除しました。\n'
                        f'日付：{income.date}\n'
                        f'カテゴリ：{income.category}\n'
                        f'金額：{income.price}円')
        return redirect(self.get_success_url())


# 月別収支グラフ
class MonthGraph(LoginRequiredMixin, TemplateView):
    template_name = 'money/month_graph.html'

    def get_context_data(self, **kwargs): # オーバーライド
        context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = '月別収支'
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

        login_user = self.request.user  # ログイン中のユーザーを取得
        # PaymentモデルのQuerySetを取り出す
        payment_queryset = Payment.objects.filter(account_id=login_user)
        payment_queryset = payment_queryset.filter(date__year=year, date__month=month)
        # 後の工程のエラー対策
        if not payment_queryset:
            return context # QuerySetが何もない時はcontextを返す
        # 取り出したQuerySetをpandasデータフレーム(df)化
        df_payment = read_frame(payment_queryset,
                        fieldnames=['date', 'price', 'category'])
        # plugin_plotly.pyのGraphGeneratorクラスでインスタンス作成
        gen_payment = GraphGenerator()

        # 月別支出円グラフ カテゴリー毎に金額をpivot集計
        df_payment_pie = pd.pivot_table(df_payment, index='category', values='price', aggfunc=np.sum)
        # カテゴリー情報をdf_payment_pie.index.valuesで取り出してリスト化
        pie_payment_labels = list(df_payment_pie.index.values)
        # 金額情報をdf_payment_pie.valuesで取り出してディクショナリ化
        pie_payment_values = [val[0] for val in df_payment_pie.values]
        plot_payment_pie = gen_payment.month_pie(labels=pie_payment_labels, values=pie_payment_values) # genインスタンスmonth_pieメソッド
        context['payment_pie'] = plot_payment_pie # contextに追加

        # テーブルでのカテゴリと集計金額の表示
        # ディクショナリ{カテゴリ:集計金額, カテゴリ:集計金額…}をcontextに追加
        context['payment_table_set'] = df_payment_pie.to_dict()['price']
        # totalの数字を計算してcontextに追加
        context['total_payment'] = df_payment['price'].sum()

        # 日別支出棒グラフの素材
        df_payment_bar = pd.pivot_table(df_payment, index='date', values='price', aggfunc=np.sum) # 日付ごとに金額をピボット集計
        dates_payment = [date.strftime('%m/%d') for date in df_payment_bar.index] # 日付情報
        heights_payment = [val[0] for val in df_payment_bar.values] # 金額情報
        plot_bar_payment = gen_payment.month_daily_bar_payment(x_list=dates_payment, y_list=heights_payment)
        context['payment_bar'] = plot_bar_payment

        # IncomeモデルのQuerySetを取り出す
        income_queryset = Income.objects.filter(account_id=login_user)
        income_queryset = income_queryset.filter(date__year=year, date__month=month)
        # 後の工程のエラー対策
        if not income_queryset:
            return context # QuerySetが何もない時はcontextを返す
        # 取り出したQuerySetをpandasデータフレーム(df)化
        df_income = read_frame(income_queryset,
                        fieldnames=['date', 'price', 'category'])
        # plugin_plotly.pyのGraphGeneratorクラスでインスタンス作成
        gen_income = GraphGenerator()

        # 月別収入円グラフ カテゴリー毎に金額をpivot集計
        df_income_pie = pd.pivot_table(df_income, index='category', values='price', aggfunc=np.sum)
        # カテゴリー情報をdf_income_pie.index.valuesで取り出してリスト化
        pie_income_labels = list(df_income_pie.index.values)
        # 金額情報をdf_income_pie.valuesで取り出してディクショナリ化
        pie_income_values = [val[0] for val in df_income_pie.values]
        # # ラベルの並び順を逆にする
        # pie_income_labels.reverse()
        plot_income_pie = gen_income.month_pie(labels=pie_income_labels, values=pie_income_values) # genインスタンスmonth_pieメソッド
        context['income_pie'] = plot_income_pie # contextに追加

        # テーブルでのカテゴリと集計金額の表示
        # ディクショナリ{カテゴリ:集計金額, カテゴリ:集計金額…}をcontextに追加
        context['income_table_set'] = df_income_pie.to_dict()['price']
        # totalの数字を計算してcontextに追加
        context['total_income'] = df_income['price'].sum()

        # 日別収入棒グラフの素材
        df_income_bar = pd.pivot_table(df_income, index='date', values='price', aggfunc=np.sum) # 日付ごとに金額をピボット集計
        dates_income = [date.strftime('%m/%d') for date in df_income_bar.index]
        heights_income = [val[0] for val in df_income_bar.values]
        plot_bar_income = gen_income.month_daily_bar_income(x_list=dates_income, y_list=heights_income)
        context['income_bar'] = plot_bar_income
        return context

# 月間推移
class TransitionView(LoginRequiredMixin, TemplateView):
    template_name = 'money/month_transition.html'

    def get_context_data(self, **kwargs): # オーバーライド
        context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = '月間推移'
        login_user = self.request.user  # ログイン中のユーザーを取得
        payment_queryset = Payment.objects.filter(account_id=login_user)
        if not payment_queryset:
            return context # QuerySetが何もない時はcontextを返す
        # 支出推移
        df_payment = read_frame(payment_queryset,
                                fieldnames=['date', 'price'])
        # 日付をdatetime化、Y/m表記に変換
        df_payment['date'] = pd.to_datetime(df_payment['date'])
        df_payment['month'] = df_payment['date'].dt.strftime('%Y/%m')
        # monthでpivot集計
        df_payment = pd.pivot_table(df_payment, index='month', values='price', aggfunc=np.sum)
        months_payment = list(df_payment.index.values) # x軸
        payments = [y[0] for y in df_payment.values] # y軸

        # 収入推移
        income_queryset = Income.objects.filter(account_id=login_user)
        df_income = read_frame(income_queryset,
                                fieldnames=['date', 'price'])
        df_income['date'] = pd.to_datetime(df_income['date'])
        df_income['month'] = df_income['date'].dt.strftime('%Y/%m')
        df_income = pd.pivot_table(df_income, index='month', values='price', aggfunc=np.sum)
        months_income = list(df_income.index.values)
        incomes = [y[0] for y in df_income.values]

        # plugin_plotly.pyのクラスでインスタンスを生成
        gen = GraphGenerator()
        context['transition_plot'] = gen.transition_plot(
                                        x_list_payment=months_payment,
                                        y_list_payment=payments,
                                        x_list_income=months_income,
                                        y_list_income=incomes
                                        )
        return context