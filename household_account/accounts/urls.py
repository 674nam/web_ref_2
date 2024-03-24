from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('familyregister/', views.FamilyregisterView.as_view(), name="familyregister"),
    path('mypage/', views.MyPageList.as_view(), name="mypage"),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('user_delete/<int:pk>/', views.UserDelete.as_view(), name='user_delete'),
]
