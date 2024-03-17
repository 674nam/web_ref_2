from django.urls import path
from . import views

app_name = 'money'

urlpatterns = [
    path('money/payment_list', views.PaymentList.as_view(), name='payment_list'),
    path('money/income_list/', views.IncomeList.as_view(), name='income_list'),
    # 支出登録、収入登録
    path('money/payment_create/', views.PaymentCreate.as_view(), name='payment_create'),
    path('money/income_create/', views.IncomeCreate.as_view(), name='income_create'),
]