from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from .models import User, Family

# ユーザー登録フォーム
class SignUpForm(UserCreationForm):
    family_name = forms.ModelChoiceField(
        label='家名',
        required=False,
        queryset=Family.objects.all(),
        widget=forms.Select(attrs={'class': 'form'})
    )
    class Meta:
        model = User # 連携するカスタムユーザーモデル
        fields = ( # フォームで使用するフィールド
            "family_name",
            "account_id",
            "email",
            "first_name",
        )

# 家名登録フォーム
class Family_registerForm(forms.Form):
    family_name = forms.CharField(label='家名',\
        widget=forms.TextInput(attrs={'class':'form'}))

# ログインフォーム
class LoginForm(AuthenticationForm):
    class Meta:
        model = User