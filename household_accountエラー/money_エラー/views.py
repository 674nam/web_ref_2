from django.views import generic
from django.urls import reverse_lazy
from .models import Payment, PaymentCategory, Income, IncomeCategory

# 支出一覧
class PaymentList(generic.ListView):
    template_name = 'money/payment_list.html'
    model = Payment
    ordering = '-date'