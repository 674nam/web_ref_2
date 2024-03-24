from django.urls import path

from . import views

app_name = 'money'

urlpatterns = [
    path('money/payment_list', views.PaymentList.as_view(), name='payment_list'),
    path('money/income_list/', views.IncomeList.as_view(), name='income_list'),
    # 支出登録、収入登録
    path('money/payment_create/', views.PaymentCreate.as_view(), name='payment_create'),
    path('money/income_create/', views.IncomeCreate.as_view(), name='income_create'),
    # ユーザー設定項目登録
    path('money/payment_item_register/', views.PaymentOrigItemRegister.as_view(), name='payment_item_register'),
    path('money/income_item_register/', views.IncomeOrigItemRegister.as_view(), name='income_item_register'),
    # 支出更新、収入更新、支出削除、収入削除
    path('money/payment_update/<int:pk>/', views.PaymentUpdate.as_view(), name='payment_update'),
    path('money/income_update/<int:pk>/', views.IncomeUpdate.as_view(), name='income_update'),
    path('money/payment_delete/<int:pk>/', views.PaymentDelete.as_view(), name='payment_delete'),
    path('money/income_delete/<int:pk>/', views.IncomeDelete.as_view(), name='income_delete'),
    # グラフ：月間収支
    path('money/month_graph/<int:year>/<int:month>/', views.MonthGraph.as_view(), name='month_graph'),
    # グラフ：月間推移
    path('money/month_transition/', views.TransitionView.as_view(), name='month_transition'),
]