from django.views.generic import *
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages # システムメッセージ
from django.contrib.auth.mixins import LoginRequiredMixin # ログインユーザーのみ閲覧可能
import numpy as np # グラフ
import pandas as pd # グラフ
from django_pandas.io import read_frame # グラフ
from django.contrib.auth import get_user_model # 設定されたユーザーモデルのインポート
# from django.core.paginator import Paginator
from django.db.models import Q

from .models import Payment, PaymentCategory, Income, IncomeCategory \
                    ,PaymentItem, IncomeItem\
                    , PaymentOrigItem, IncomeOrigItem
from .forms import PaymentSearchForm, IncomeSearchForm \
                    , PaymentCreateForm, IncomeCreateForm \
                    , PaymentOrigItemForm, IncomeOrigItemForm \
                    # , TransitionGraphSearchForm
from .plugin_plotly import GraphGenerator # グラフ

# 支出一覧
class PaymentList(LoginRequiredMixin, ListView):
    # template_name = 'money/payment_list.html'
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
    # template_name = 'money/income_list.html'
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

# 支出登録
# class PaymentCreate(LoginRequiredMixin, CreateView):
#     template_name = 'money/create.html'
#     model = Payment
#     form_class = PaymentCreateForm

#     def get_context_data(self, **kwargs): #オーバーライド
#         context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
#         context['page_title'] = '支出登録' # contextに追加
#         return context

#     def get_success_url(self):
#         return reverse_lazy('money:payment_list')

#     def form_valid(self, form):
#         # self.object = payment = form.save()
#         login_user = self.request.user  # ログイン中のユーザーを取得
#         self.object = payment = form.save(commit=False)
#         payment.account_id = login_user
#         payment.save()
#         messages.info(self.request,
#                         f'支出を登録しました'
#                         f'日付:{payment.date}'
#                         f'カテゴリ:{payment.category}'
#                         f'金額:{payment.price}円')
#         return redirect(self.get_success_url())

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
                        f'支出を登録しました'
                        f'日付:{payment.date}'
                        f'カテゴリ:{payment.category}'
                        f'金額:{payment.price}円')
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
                        f'収入を登録しました'
                        f'日付:{income.date}'
                        f'カテゴリ:{income.category}'
                        f'金額:{income.price}円')
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
                        f'支出を更新しました'
                        f'日付:{payment.date}'
                        f'カテゴリ:{payment.category}'
                        f'金額:{payment.price}円')
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
                        f'収入を更新しました'
                        f'日付:{income.date}'
                        f'カテゴリ:{income.category}'
                        f'金額:{income.price}円')
        return redirect(self.get_success_url())

# 支出削除
class PaymentDelete(LoginRequiredMixin, DeleteView):
    template_name = 'money/delete.html'
    model = Payment

    def get_context_data(self, **kwargs): # オーバーライド
        context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = '支出削除' # contextに追加
        return context

    def get_success_url(self):
        return reverse_lazy('money:payment_list')

    def delete(self, request, *args, **kwargs):
        self.object = payment = self.get_object()
        payment.delete()
        messages.info(self.request,
                        f'支出を削除しました'
                        f'日付:{payment.date}'
                        f'カテゴリ:{payment.category}'
                        f'金額:{payment.price}円')
        return redirect(self.get_success_url())

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

    def delete(self, request, *args, **kwargs):
        self.object = income = self.get_object()
        income.delete()
        messages.info(self.request,
                        f'収入を削除しました'
                        f'日付:{income.date}'
                        f'カテゴリ:{income.category}'
                        f'金額:{income.price}円')
        return redirect(self.get_success_url())


# 月間収支グラフ
class MonthGraph(LoginRequiredMixin, TemplateView):
    template_name = 'money/month_graph.html'

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

        # 月間支出円グラフ カテゴリー毎に金額をpivot集計
        df_payment_pie = pd.pivot_table(df_payment, index='category', values='price', aggfunc=np.sum)
        # カテゴリー情報をdf_payment_pie.index.valuesで取り出してリスト化
        pie_payment_labels = list(df_payment_pie.index.values)
        # 金額情報をdf_payment_pie.valuesで取り出してディクショナリ化
        pie_payment_values = [val[0] for val in df_payment_pie.values]
        # ラベルの並び順を逆にする
        pie_payment_labels.reverse()
        plot_payment_pie = gen_payment.month_pie(labels=pie_payment_labels, values=pie_payment_values) # genインスタンスmonth_pieメソッド
        context['payment_pie'] = plot_payment_pie # contextに追加

        # テーブルでのカテゴリと集計金額の表示
        # ディクショナリ{カテゴリ:集計金額, カテゴリ:集計金額…}をcontextに追加
        context['payment_table_set'] = df_payment_pie.to_dict()['price']
        # totalの数字を計算してcontextに追加
        context['total_payment'] = df_payment['price'].sum()

        # 日別支出棒グラフの素材
        df_payment_bar = pd.pivot_table(df_payment, index='date', values='price', aggfunc=np.sum) # 日付ごとに金額をピボット集計
        # 日付のフォーマットを変更する
        dates_payment = [date.strftime('%m/%d') for date in df_payment_bar.index]
        # dates_payment = list(df_payment_bar.index.values) # 日付情報をリスト化
        heights_payment = [val[0] for val in df_payment_bar.values] # 金額情報をディクショナリ化
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

        # 月間収入円グラフ カテゴリー毎に金額をpivot集計
        df_income_pie = pd.pivot_table(df_income, index='category', values='price', aggfunc=np.sum)
        # カテゴリー情報をdf_income_pie.index.valuesで取り出してリスト化
        pie_income_labels = list(df_income_pie.index.values)
        # 金額情報をdf_income_pie.valuesで取り出してディクショナリ化
        pie_income_values = [val[0] for val in df_income_pie.values]
        # ラベルの並び順を逆にする
        pie_income_labels.reverse()
        plot_income_pie = gen_income.month_pie(labels=pie_income_labels, values=pie_income_values) # genインスタンスmonth_pieメソッド
        context['income_pie'] = plot_income_pie # contextに追加

        # テーブルでのカテゴリと集計金額の表示
        # ディクショナリ{カテゴリ:集計金額, カテゴリ:集計金額…}をcontextに追加
        context['income_table_set'] = df_income_pie.to_dict()['price']
        # totalの数字を計算してcontextに追加
        context['total_income'] = df_income['price'].sum()

        # 日別収入棒グラフの素材
        df_income_bar = pd.pivot_table(df_income, index='date', values='price', aggfunc=np.sum) # 日付ごとに金額をピボット集計
                # 日付のフォーマットを変更する
        dates_income = [date.strftime('%m/%d') for date in df_income_bar.index]
        # dates_income = list(df_income_bar.index.values) # 日付情報をリスト化
        heights_income = [val[0] for val in df_income_bar.values] # 金額情報をディクショナリ化
        plot_bar_income = gen_income.month_daily_bar_income(x_list=dates_income, y_list=heights_income)
        context['income_bar'] = plot_bar_income

        return context


# # 月間支出
# class MonthGraph(LoginRequiredMixin, TemplateView):
#     template_name = 'money/month_graph.html'

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
#         df_payment_pie = pd.pivot_table(df, index='category', values='price', aggfunc=np.sum)
#         # カテゴリー情報をdf_payment_pie.index.valuesで取り出してリスト化
#         pie_payment_labels = list(df_payment_pie.index.values)
#         # 金額情報をdf_payment_pie.valuesで取り出してディクショナリ化
#         pie_payment_values = [val[0] for val in df_payment_pie.values]
#         plot_payment_pie = gen.month_pie(labels=pie_payment_labels, values=pie_payment_values) # genインスタンスmonth_pieメソッド
#         context['payment_pie'] = plot_payment_pie # contextに追加

#         # テーブルでのカテゴリと集計金額の表示
#         # ディクショナリ{カテゴリ:集計金額, カテゴリ:集計金額…}をcontextに追加
#         context['payment_table_set'] = df_payment_pie.to_dict()['price']
#         # totalの数字を計算してcontextに追加
#         context['total_payment'] = df['price'].sum()

#         # 日別棒グラフの素材
#         df_payment_bar = pd.pivot_table(df, index='date', values='price', aggfunc=np.sum) # 日付ごとに金額をピボット集計
#         dates_payment = list(df_payment_bar.index.values) # 日付情報をリスト化
#         heights_payment = [val[0] for val in df_payment_bar.values] # 金額情報をディクショナリ化
#         plot_bar_payment = gen.month_daily_bar(x_list=dates_payment, y_list=heights_payment)
#         context['payment_bar'] = plot_bar_payment
#         return context

# # 月間支出・収入グラフ
# class MonthGraph(LoginRequiredMixin, TemplateView):
#     template_name = 'money/month_graph.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         year = int(self.kwargs.get('year'))
#         month = int(self.kwargs.get('month'))
#         context['year_month'] = f'{year}年{month}月'

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
#         context['prev_year'] = prev_year
#         context['prev_month'] = prev_month
#         context['next_year'] = next_year
#         context['next_month'] = next_month

#         login_user = self.request.user  # ログイン中のユーザーを取得

#         # PaymentモデルのうちログインユーザーのQuerySetを取り出す
#         payment_queryset = Payment.objects.filter(account_id=login_user)
#         payment_queryset = payment_queryset.filter(date__year=year, date__month=month)
#         # 後の工程のエラー対策
#         if not payment_queryset:
#             return context
#         # 取り出したQuerySetをpandasデータフレーム(df)化
#         payment_df = read_frame(payment_queryset, fieldnames=['date', 'price', 'category'])

#         # IncomeモデルのうちログインユーザーのQuerySetを取り出す
#         income_queryset = Income.objects.filter(account_id=login_user)
#         income_queryset = income_queryset.filter(date__year=year, date__month=month)
#         if not income_queryset:
#             return context
#         income_df = read_frame(income_queryset, fieldnames=['date', 'price', 'category'])

#         # plugin_plotly.pyのGraphGeneratorクラスでインスタンス作成
#         gen = GraphGenerator()

#         # Paymentデータに基づくグラフ
#         payment_pie_payment_labels, payment_pie_payment_values = self.prepare_data(payment_df)
#         payment_pie = gen.month_pie(labels=payment_pie_payment_labels, values=payment_pie_payment_values)
#         context['payment_pie'] = payment_pie
#         # カテゴリー毎に金額をpivot集計
#         payment_table_set = pd.pivot_table(payment_df, index='category', values='price', aggfunc=np.sum)
#         # テーブルでのカテゴリと集計金額の表示
#         # ディクショナリ{カテゴリ:集計金額, カテゴリ:集計金額…}をcontextに追加
#         context['payment_table_set'] = payment_table_set.to_dict()['price']
#         # totalの数字を計算してcontextに追加
#         context['total_payment'] = payment_df['price'].sum()
#         # 日別棒グラフ
#         payment_bar_dates_payment, payment_bar_heights_payment = self.prepare_data(payment_df, by='date')
#         payment_bar = gen.month_daily_bar_payment(x_list=payment_bar_dates_payment, y_list=payment_bar_heights_payment)
#         context['payment_bar'] = payment_bar

#         # Incomeデータに基づくグラフ
#         income_pie_payment_labels, income_pie_payment_values = self.prepare_data(income_df)
#         income_pie = gen.month_pie(labels=income_pie_payment_labels, values=income_pie_payment_values)
#         context['income_pie'] = income_pie

#         income_table_set = pd.pivot_table(income_df, index='category', values='price', aggfunc=np.sum)
#         context['income_table_set'] = income_table_set.to_dict()['price']
#         context['total_income'] = income_df['price'].sum()

#         income_bar_dates_payment, income_bar_heights_payment = self.prepare_data(income_df, by='date')
#         income_bar = gen.month_daily_bar_income(x_list=income_bar_dates_payment, y_list=income_bar_heights_payment)
#         context['income_bar'] = income_bar

#         return context

#     def prepare_data(self, df, by='category'):
#         if by == 'category':
#             pivot_df = pd.pivot_table(df, index=by, values='price', aggfunc=np.sum)
#             labels = list(pivot_df.index.values)
#             values = [val[0] for val in pivot_df.values]
#             return labels, values
#         elif by == 'date':
#             pivot_df = pd.pivot_table(df, index='date', values='price', aggfunc=np.sum)
#             dates_payment = list(pivot_df.index.values)
#             heights_payment = [val[0] for val in pivot_df.values]
#             return dates_payment, heights_payment
