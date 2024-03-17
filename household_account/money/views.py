from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages # システムメッセージ
from django.contrib.auth.mixins import LoginRequiredMixin # ログインユーザーのみ閲覧可能

from .models import Payment, PaymentCategory, Income, IncomeCategory
from .forms import PaymentSearchForm, IncomeSearchForm \
                    , PaymentCreateForm, IncomeCreateForm \
                    # , TransitionGraphSearchForm

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
