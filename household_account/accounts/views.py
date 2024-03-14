from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import SignUpForm, LoginForm #, Family_registerForm

# ホーム
class IndexView(TemplateView):
    template_name = "index.html"

# ユーザー登録
class SignupView(CreateView):
    form_class = SignUpForm   # 登録用フォームを設定
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:index") # ユーザー作成後のリダイレクト先ページ

    def form_valid(self, form): # ユーザー作成後にそのままログイン状態にする
        response = super().form_valid(form)
        account_id = form.cleaned_data.get("account_id")
        password = form.cleaned_data.get("password1")
        user = authenticate(account_id=account_id, password=password)
        login(self.request, user)
        messages.success(self.request, '新規ユーザーを登録しました。')
        return response

# # 家名登録用
# class Family_registerView(CreateView):
#     form_class = Family_registerForm   # 登録用フォームを設定
#     template_name = "accounts/family_register.html"
#     success_url = reverse_lazy("accounts:signup") # 家名登録後のリダイレクト先ページ

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     family_name = form.cleaned_data.get("family_name")
    #     messages.success(self.request, '新規ユーザーを登録しました。')
    #     return response


# ログイン
class LoginView(BaseLoginView):
    form_class = LoginForm      # ログイン用フォームを設定
    template_name = "accounts/login.html"
# ログアウト
class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("accounts:index")