from django.urls import path
from . import views

app_name = 'money'

urlpatterns = [
    path('money/payment_list', views.PaymentList.as_view(), name='payment_list'),
]