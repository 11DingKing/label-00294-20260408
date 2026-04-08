"""
认证模块视图
"""
import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from .serializers import LoginSerializer, UserSerializer

logger = logging.getLogger('apps')


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    用户登录
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # 生成JWT Token
        refresh = RefreshToken.for_user(user)
        
        # 记录登录日志
        logger.info(f"User {user.username} logged in successfully")
        
        return Response({
            'code': 200,
            'message': '登录成功',
            'data': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': UserSerializer(user).data
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'code': 400,
        'message': serializer.errors.get('non_field_errors', ['登录失败'])[0],
        'data': None
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    用户退出
    """
    try:
        # 获取refresh token并加入黑名单
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                logger.warning(f"Token blacklist error: {str(e)}")
        
        # 记录退出日志
        logger.info(f"User {request.user.username} logged out")
        
        return Response({
            'code': 200,
            'message': '退出成功',
            'data': None
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return Response({
            'code': 400,
            'message': '退出失败',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info_view(request):
    """
    获取当前用户信息
    """
    return Response({
        'code': 200,
        'message': '获取成功',
        'data': UserSerializer(request.user).data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    修改密码
    """
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response({
            'code': 400,
            'message': '请提供旧密码和新密码',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if len(new_password) < 6:
        return Response({
            'code': 400,
            'message': '新密码长度不能少于6位',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    if not user.check_password(old_password):
        return Response({
            'code': 400,
            'message': '旧密码错误',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    logger.info(f"User {user.username} changed password")
    
    return Response({
        'code': 200,
        'message': '密码修改成功',
        'data': None
    }, status=status.HTTP_200_OK)
