from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView, ListView \
                                , UpdateView, DeleteView
from django.contrib.auth.views import LoginView as BaseLoginView \
                                    , LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin # ログインユーザーのみ閲覧可能
from django.shortcuts import render, redirect

from .forms import SignUpForm, LoginForm, FamilyregisterForm
from .models import User

# ホーム
class IndexView(TemplateView):
    template_name = "accounts/login.html"

# ユーザー登録
class SignupView(CreateView):
    form_class = SignUpForm   # 登録用フォームを設定
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("money:payment_list") # ユーザー作成後のリダイレクト先

    def form_valid(self, form): # ユーザー作成後にそのままログイン状態にする
        response = super().form_valid(form)
        account_id = form.cleaned_data.get("account_id")
        password = form.cleaned_data.get("password1")
        user = authenticate(account_id=account_id, password=password)
        login(self.request, user)
        messages.success(self.request, '新規ユーザーを登録しました。')
        return response

# 家名登録用
class FamilyregisterView(CreateView):
    form_class = FamilyregisterForm   # 登録用フォームを設定
    template_name = "accounts/familyregister.html"
    success_url = reverse_lazy("accounts:signup") # 家名登録後のリダイレクト先ページ

#  マイページ
class MyPageList(LoginRequiredMixin, ListView):
    template_name = 'accounts/mypage.html'
    model = User

    def get_queryset(self):
        login_user = self.request.user  # ログイン中のユーザーを取得
        queryset = super().get_queryset() # PaymentList.objects.all()と同等
        queryset = queryset.filter(account_id=login_user)
        return queryset

    def get_context_data(self, **kwargs): # オーバーライド
        context = super().get_context_data(**kwargs)  # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = 'マイページ'
        return context # テンプレートへcontextを渡す

# ユーザー情報更新
class UserUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/user_update.html'
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy("accounts:mypage") # ユーザー更新後のリダイレクト先

    def get_context_data(self, **kwargs): # オーバーライド
        context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = 'ユーザー情報更新' # contextに追加
        return context

    def form_valid(self, form): # ユーザー更新後にそのままログイン状態にする
        self.object = form.save()
        response = super().form_valid(form)
        account_id = form.cleaned_data.get("account_id")
        password = form.cleaned_data.get("password1")
        user = authenticate(account_id=account_id, password=password)
        login(self.request, user)
        messages.success(self.request, 'ユーザー情報を更新しました。')
        return response

# ユーザー削除
class UserDelete(LoginRequiredMixin, DeleteView):
    template_name = 'accounts/user_delete.html'
    model = User

    def get_context_data(self, **kwargs): # オーバーライド
        context = super().get_context_data(**kwargs) # 親クラスの get_context_dataメソッドを実行
        context['page_title'] = 'ユーザー削除' # contextに追加
        return context

    def post(self, request, *args, **kwargs):
        self.object = user = self.get_object()
        user.delete()
        messages.info(request,'ユーザーを削除しました。')
        return redirect(reverse_lazy('accounts:login'))


# ログイン
class LoginView(BaseLoginView):
    form_class = LoginForm      # ログイン用フォームを設定
    template_name = "accounts/login.html"

# ログアウト
class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("accounts:login")