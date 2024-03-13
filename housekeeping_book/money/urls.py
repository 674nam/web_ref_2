from django.urls import path
from . import views

app_name = 'money'
urlpatterns = [
        path('', views.index, name='index'),
        path('<int:year>/<int:month>', views.index, name='index'),

        # path('', views.MainView.as_view(), name='index'), # Viewクラス使用時
        # path('<int:year>/<int:month>', views.MainView.as_view(), name='index'), # Viewクラス使用時
        ]