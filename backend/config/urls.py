"""
URL configuration for order management system.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
