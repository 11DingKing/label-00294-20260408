"""
认证模块路由
"""
from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.user_info_view, name='user-info'),
    path('change-password/', views.change_password_view, name='change-password'),
]
