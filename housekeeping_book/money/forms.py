from django import forms
from .models import Money

class SpendingForm(forms.Form):
    choices = (
        ('食費', '食費'),
        ('雑貨', '雑貨'),
        ('消耗品', '消耗品'),
        ('交通費', '交通費'),
        ('娯楽', '娯楽'),
        )

    use_date = forms.DateTimeField(label='日付(yyyy/mm/dd)')
    cost = forms.IntegerField(label='金額(数値)')
    category = forms.ChoiceField(choices=choices, label='カテゴリー')
    detail = forms.CharField(
            max_length=200,
            label='備考'
            )
