from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django import forms
from django.forms import ModelForm
from django import forms

from .models import CustomUser, Family

# ユーザー登録フォーム
class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser # 連携するカスタムユーザーモデル
        fields = ( # フォームで使用するフィールド
            "family_name",
            "username",
            "email",
            "first_name",
        )


# 家名登録フォーム
class FamilyregisterForm(ModelForm):
    class Meta:
        model = Family
        fields = ['family_name']

# ログインフォーム
class LoginForm(AuthenticationForm): # ログインフォームを追加
    class Meta:
        model = CustomUser