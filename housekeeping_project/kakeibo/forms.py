from django import forms
from .models import PaymentCategory, Payment, Income, IncomeCategory
from django.utils import timezone

# 支出検索フォーム
class PaymentSearchForm(forms.Form):

    # 年の選択肢を動的に作る
    start_year = 2019  # 家計簿の登録を始めた年
    end_year = timezone.now().year + 1  # 現在の年＋１年
    years = [(year, f'{year}年') for year in reversed(range(start_year, end_year + 1))]
    years.insert(0, (0, ''))  # 空白の選択を追加
    YEAR_CHOICES = tuple(years)

    # 月の選択肢を動的に作る
    months = [(month, f'{month}月') for month in range(1, 13)]
    months.insert(0, (0, ''))
    MONTH_CHOICES = tuple(months)

    # 年の選択
    year = forms.ChoiceField(
        label='年での絞り込み',
        required=False,
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form'})
    )

    # 月の選択
    month = forms.ChoiceField(
        label='月での絞り込み',
        required=False,
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={'class': 'form'})
    )

    # 〇〇円以上
    greater_than = forms.IntegerField(
        label='Greater Than',
        required=False,
        widget=forms.TextInput(attrs={
                    'class': 'form',
                    'autocomplete': 'off',
                    'placeholder': '〇〇円以上'})
    )

    # 〇〇円以下
    less_than = forms.IntegerField(
        label='Less Than',
        required=False,
        widget=forms.TextInput(attrs={
                    'class': 'form',
                    'autocomplete': 'off',
                    'placeholder': '〇〇円以下'})
    )

    # キーワード
    key_word = forms.CharField(
        label='検索キーワード',
        required=False,
        widget=forms.TextInput(attrs={
                    'class': 'form',
                    'autocomplete': 'off',
                    'placeholder': 'キーワード',})
    )

    # カテゴリー検索
    category = forms.ModelChoiceField(
        label='カテゴリでの絞り込み',
        required=False,
        queryset=PaymentCategory.objects.order_by('name'),
        widget=forms.Select(attrs={'class': 'form'}),
    )

# 収入検索フォーム
class IncomeSearchForm(forms.Form):
    start_year = 2019
    end_year = timezone.now().year + 1
    years = [(year, f'{year}年') for year in reversed(range(start_year, end_year + 1))]
    years.insert(0, (0, ''))
    YEAR_CHOICES = tuple(years)

    months = [(month, f'{month}月') for month in range(1, 13)]
    months.insert(0, (0, ''))
    MONTH_CHOICES = tuple(months)

    year = forms.ChoiceField(
        label='年での絞り込み',
        required=False,
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form', 'value': ''})
    )
    month = forms.ChoiceField(
        label='月での絞り込み',
        required=False,
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={'class': 'form'})
    )

# 支出登録フォーム
class PaymentCreateForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['autocomplete'] = 'off'

# 収入登録フォーム
class IncomeCreateForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['autocomplete'] = 'off'

# 推移グラフの絞り込みフォーム
class TransitionGraphSearchForm(forms.Form):
    SHOW_CHOICES = (
        ('Payment', 'Payment'),
        ('Income', 'Income'),
    )

    payment_category = forms.ModelChoiceField(
        label='支出カテゴリでの絞り込み',
        required=False,
        queryset=PaymentCategory.objects.order_by('name'),
        # widget=CustomRadioSelect,
    )

    income_category = forms.ModelChoiceField(
        label='収入カテゴリでの絞り込み',
        required=False,
        queryset=IncomeCategory.objects.order_by('name'),
        # widget=CustomRadioSelect,
    )

    graph_visible = forms.ChoiceField(
                        required=False,
                        label='表示グラフ',
                        choices=SHOW_CHOICES,
                    #   widget=CustomRadioSelect
                        )
