"""
用户模块测试用例
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class UserTestCase(TestCase):
    """用户模块测试"""
    
    def setUp(self):
        """测试前置设置"""
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com',
            is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username='normal',
            password='normal123',
            email='normal@example.com',
            is_staff=False
        )
        
        self.users_url = '/api/users/'
    
    def test_get_users_list_as_admin(self):
        """测试管理员获取用户列表"""
        # 管理员登录
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        login_response = self.client.post('/api/auth/login/', login_data, format='json')
        access_token = login_response.data['data']['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        
        response = self.client.get(self.users_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 应该返回用户列表
        if 'results' in response.data:
            self.assertGreaterEqual(len(response.data['results']), 2)
        else:
            self.assertGreaterEqual(len(response.data), 2)
    
    def test_get_users_list_as_normal_user(self):
        """测试普通用户无法获取用户列表"""
        # 普通用户登录
        login_data = {
            'username': 'normal',
            'password': 'normal123'
        }
        login_response = self.client.post('/api/auth/login/', login_data, format='json')
        access_token = login_response.data['data']['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        
        response = self.client.get(self.users_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_users_list_unauthorized(self):
        """测试未认证无法获取用户列表"""
        client = APIClient()
        response = client.get(self.users_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
