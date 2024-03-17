from django import forms
from django.utils import timezone

from accounts.models import User
from .models import PaymentCategory, IncomeCategory, Payment, Income

# 支出検索フォーム
class PaymentSearchForm(forms.Form):
    # 年の選択肢を動的に作る
    start_year = 2020  # 家計簿の登録開始年
    end_year = timezone.now().year + 1  # 現在の年の１年先まで表示
    years = [(year, f'{year}年') for year in reversed(range(start_year, end_year + 1))]
    years.insert(0, (0, ''))  # 空白の選択を追加
    year_choices = tuple(years)

    # 月の選択肢を動的に作る
    months = [(month, f'{month}月') for month in range(1, 13)]
    months.insert(0, (0, ''))
    month_choices = tuple(months)

    # 年の選択
    year = forms.ChoiceField(
        label='年での絞り込み',
        required=False,
        choices=year_choices,
        widget=forms.Select(attrs={'class': 'form'})
    )

    # 月の選択
    month = forms.ChoiceField(
        label='月での絞り込み',
        required=False,
        choices=month_choices,
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

    # カテゴリー
    category = forms.ModelChoiceField(
        label='カテゴリでの絞り込み',
        required=False,
        queryset=PaymentCategory.objects.order_by('id'),
        widget=forms.Select(attrs={'class': 'form'}),
    )

    # 特定のユーザー
    account_id = forms.ModelChoiceField(
        label='Account',
        required=False,
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form'}),
    )


# 収入検索フォーム
class IncomeSearchForm(forms.Form):
    # 年の選択肢を動的に作る
    start_year = 2020  # 家計簿の登録開始年
    end_year = timezone.now().year + 1  # 現在の年の１年先まで表示
    years = [(year, f'{year}年') for year in reversed(range(start_year, end_year + 1))]
    years.insert(0, (0, ''))  # 空白の選択を追加
    year_choices = tuple(years)

    # 月の選択肢を動的に作る
    months = [(month, f'{month}月') for month in range(1, 13)]
    months.insert(0, (0, ''))
    month_choices = tuple(months)

    # 年の選択
    year = forms.ChoiceField(
        label='年での絞り込み',
        required=False,
        choices=year_choices,
        widget=forms.Select(attrs={'class': 'form'})
    )

    # 月の選択
    month = forms.ChoiceField(
        label='月での絞り込み',
        required=False,
        choices=month_choices,
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

    # カテゴリー
    category = forms.ModelChoiceField(
        label='カテゴリでの絞り込み',
        required=False,
        queryset=IncomeCategory.objects.order_by('id'),
        widget=forms.Select(attrs={'class': 'form'}),
    )

    # 特定のユーザー
    account_id = forms.ModelChoiceField(
        label='Account',
        required=False,
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form'}),
    )


# 支出登録フォーム
class PaymentCreateForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})  # 備考欄の大きさを3行に設定
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form'
            # field.widget.attrs['placeholder'] = field.label フォーム内文字
            field.widget.attrs['autocomplete'] = 'off'

# 収入登録フォーム
class IncomeCreateForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'
        widgets = {
        'description': forms.Textarea(attrs={'rows': 3})  # 備考欄の大きさを3行に設定
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form'
            # field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['autocomplete'] = 'off'
