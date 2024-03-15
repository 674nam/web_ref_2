from django.views import generic
from .models import Payment, PaymentCategory, Income, IncomeCategory
from .forms import PaymentSearchForm

class PaymentList(generic.ListView):
    template_name = 'money/payment_list.html' # レンダリングするテンプレート
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
        context['search_form'] = self.form  # search_form変数をcontextに追加

        return context # テンプレートをcontextに渡す{{ search_form }}で使用
