from django.urls import path

from . import views
from money.views import *

app_name = "accounts"

urlpatterns = [
    # path("", views.IndexView.as_view(), name="index"),
    path('', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('familyregister/', views.FamilyregisterView.as_view(), name="familyregister"),
    # 家計簿アプリへ
    path('money/payment_list/', PaymentList.as_view(), name='payment_list'),
    path('money/payment_create/', PaymentCreate.as_view(), name='payment_create'),
]
