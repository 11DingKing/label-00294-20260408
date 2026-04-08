"""
认证模块序列化器
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField(
        required=True,
        help_text="用户名"
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        help_text="密码"
    )
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('用户名或密码错误')
            if not user.is_active:
                raise serializers.ValidationError('用户账户已被禁用')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('必须提供用户名和密码')
        
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id', 'is_staff']
