"""
用户模块路由
"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list_view, name='user-list'),
]
