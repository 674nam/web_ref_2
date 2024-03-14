from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User, Family

# ユーザー登録フォーム
class SignUpForm(UserCreationForm):
    class Meta:
        model = User # 連携するカスタムユーザーモデル
        fields = ( # フォームで使用するフィールド
            "family_name",
            "account_id",
            "email",
            "first_name",
        )

# # 家名登録フォーム
# class Family_registerForm(forms.Form):
#     family_name = forms.CharField(label='家名',\
#         widget=forms.TextInput(attrs={'class':'form'}))

# ログインフォーム
class LoginForm(AuthenticationForm): # ログインフォームを追加
    class Meta:
        model = User