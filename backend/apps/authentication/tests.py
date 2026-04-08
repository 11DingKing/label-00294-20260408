"""
认证模块测试用例
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class LoginTestCase(APITestCase):
    """登录接口测试"""
    
    def setUp(self):
        """测试前准备"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.login_url = '/api/auth/login/'
    
    def test_login_success(self):
        """测试登录成功"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 200)
        self.assertIn('access_token', response.data['data'])
        self.assertIn('refresh_token', response.data['data'])
        self.assertIn('user', response.data['data'])
    
    def test_login_wrong_password(self):
        """测试密码错误"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 400)
    
    def test_login_user_not_exist(self):
        """测试用户不存在"""
        data = {
            'username': 'nonexistent',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_missing_fields(self):
        """测试缺少必填字段"""
        response = self.client.post(self.login_url, {'username': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_inactive_user(self):
        """测试禁用用户登录"""
        self.user.is_active = False
        self.user.save()
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutTestCase(APITestCase):
    """退出接口测试"""
    
    def setUp(self):
        """测试前准备"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        self.logout_url = '/api/auth/logout/'
    
    def test_logout_success(self):
        """测试退出成功"""
        data = {'refresh_token': str(self.refresh)}
        response = self.client.post(self.logout_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 200)
    
    def test_logout_without_token(self):
        """测试无token退出"""
        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_logout_unauthorized(self):
        """测试未认证退出"""
        self.client.credentials()  # 清除认证
        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserInfoTestCase(APITestCase):
    """用户信息接口测试"""
    
    def setUp(self):
        """测试前准备"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        self.user_info_url = '/api/auth/user/'
    
    def test_get_user_info_success(self):
        """测试获取用户信息成功"""
        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 200)
        self.assertEqual(response.data['data']['username'], 'testuser')
        self.assertEqual(response.data['data']['email'], 'test@example.com')
    
    def test_get_user_info_unauthorized(self):
        """测试未认证获取用户信息"""
        self.client.credentials()
        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChangePasswordTestCase(APITestCase):
    """修改密码接口测试"""
    
    def setUp(self):
        """测试前准备"""
        self.user = User.objects.create_user(
            username='testuser',
            password='oldpass123'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        self.change_password_url = '/api/auth/change-password/'
    
    def test_change_password_success(self):
        """测试修改密码成功"""
        data = {
            'old_password': 'oldpass123',
            'new_password': 'newpass456'
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 200)
        
        # 验证新密码可以登录
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass456'))
    
    def test_change_password_wrong_old_password(self):
        """测试旧密码错误"""
        data = {
            'old_password': 'wrongpass',
            'new_password': 'newpass456'
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_change_password_short_new_password(self):
        """测试新密码太短"""
        data = {
            'old_password': 'oldpass123',
            'new_password': '123'
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_change_password_missing_fields(self):
        """测试缺少必填字段"""
        response = self.client.post(self.change_password_url, {'old_password': 'oldpass123'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_change_password_unauthorized(self):
        """测试未认证修改密码"""
        self.client.credentials()
        data = {
            'old_password': 'oldpass123',
            'new_password': 'newpass456'
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
