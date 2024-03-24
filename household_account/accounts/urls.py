from django.urls import path

from . import views
from money.views import PaymentList, PaymentCreate

app_name = "accounts"

urlpatterns = [
    # path("", views.IndexView.as_view(), name="index"), # 不要
    path('', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('familyregister/', views.FamilyregisterView.as_view(), name="familyregister"),

    path('mypage/', views.MyPageList.as_view(), name="mypage"),
    path('user_delete/<int:pk>/', views.UserDelete.as_view(), name='user_delete'),

    # # 家計簿アプリへ
    # path('money/payment_list/', PaymentList.as_view(), name='payment_list'),
    # path('money/payment_create/', PaymentCreate.as_view(), name='payment_create'),
]
