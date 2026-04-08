"""
用户模块视图
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.authentication.serializers import UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list_view(request):
    """
    获取用户列表（仅管理员）
    """
    from django.contrib.auth.models import User
    from rest_framework.pagination import PageNumberPagination
    
    if not request.user.is_staff:
        return Response({
            'code': 403,
            'message': '权限不足',
            'data': None
        }, status=status.HTTP_403_FORBIDDEN)
    
    paginator = PageNumberPagination()
    paginator.page_size = 10
    users = User.objects.all()
    paginated_users = paginator.paginate_queryset(users, request)
    
    serializer = UserSerializer(paginated_users, many=True)
    return paginator.get_paginated_response(serializer.data)
