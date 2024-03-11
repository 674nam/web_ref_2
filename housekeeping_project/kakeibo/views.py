from django.views import generic

from .models import Payment, PaymentCategory, Income, IncomeCategory
from .forms import PaymentSearchForm, IncomeSearchForm # 検索フォーム用


class PaymentList(generic.ListView):
    template_name = 'kakeibo/payment_list.html'
    model = Payment
    ordering = '-date'
    # paginate_by = 5 # ページネーション作成中

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = PaymentSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            # 選択なし -> 文字列'0'が入るため除外
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            # 選択なし -> 文字列'0'が入るため除外
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form  # search formを渡す

        return context


class IncomeList(generic.ListView):
    template_name = 'kakeibo/income_list.html'
    model = Income
    ordering = '-date'
    # paginate_by = 5 # ページネーション作成中

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