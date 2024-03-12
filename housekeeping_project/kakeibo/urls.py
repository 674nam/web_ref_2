from django.urls import path
from . import views

app_name = 'kakeibo'

urlpatterns = [
    # 支出一覧、収入一覧
    path('', views.PaymentList.as_view(), name='payment_list'),
    path('income_list/', views.IncomeList.as_view(), name='income_list'),
    # 支出登録、収入登録
    path('payment_create/', views.PaymentCreate.as_view(), name='payment_create'),
    path('income_create/', views.IncomeCreate.as_view(), name='income_create'),
    # 支出更新、収入更新、支出削除、収入削除
    path('payment_update/<int:pk>/', views.PaymentUpdate.as_view(), name='payment_update'),
    path('income_update/<int:pk>/', views.IncomeUpdate.as_view(), name='income_update'),
    path('payment_delete/<int:pk>/', views.PaymentDelete.as_view(), name='payment_delete'),
    path('income_delete/<int:pk>/', views.IncomeDelete.as_view(), name='income_delete'),
    # グラフ：月間支出ダッシュボード
    path('month_dashboard/<int:year>/<int:month>/', views.MonthDashboard.as_view(), name='month_dashboard'),
    # グラフ：月毎の収支推移
    path('transition/', views.TransitionView.as_view(), name='transition'),
]