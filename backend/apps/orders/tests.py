"""
订单模块测试用例
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Order, OrderItem


class OrderModelTestCase(TestCase):
    """订单模型测试"""
    
    def setUp(self):
        """测试前准备"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_order_creation(self):
        """测试订单创建"""
        order = Order.objects.create(
            user=self.user,
            shipping_address='北京市朝阳区',
            contact_phone='13800138000'
        )
        self.assertIsNotNone(order.order_number)
        self.assertTrue(order.order_number.startswith('ORD'))
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.total_amount, Decimal('0.00'))
    
    def test_order_number_unique(self):
        """测试订单号唯一性"""
        order1 = Order.objects.create(
            user=self.user,
            shipping_address='地址1',
            contact_phone='13800138001'
        )
        order2 = Order.objects.create(
            user=self.user,
            shipping_address='地址2',
            contact_phone='13800138002'
        )
        self.assertNotEqual(order1.order_number, order2.order_number)
    
    def test_order_item_subtotal_calculation(self):
        """测试订单项小计计算"""
        order = Order.objects.create(
            user=self.user,
            shipping_address='北京市',
            contact_phone='13800138000'
        )
        item = OrderItem.objects.create(
            order=order,
            product_name='测试商品',
            price=Decimal('99.00'),
            quantity=2
        )
        self.assertEqual(item.subtotal, Decimal('198.00'))
    
    def test_order_total_amount_update(self):
        """测试订单总额更新"""
        order = Order.objects.create(
            user=self.user,
            shipping_address='北京市',
            contact_phone='13800138000'
        )
        OrderItem.objects.create(
            order=order,
            product_name='商品1',
            price=Decimal('100.00'),
            quantity=2
        )
        OrderItem.objects.create(
            order=order,
            product_name='商品2',
            price=Decimal('50.00'),
            quantity=1
        )
        order.refresh_from_db()
        self.assertEqual(order.total_amount, Decimal('250.00'))


class OrderAPITestCase(APITestCase):
    """订单API测试"""
    
    def setUp(self):
        """测试前准备"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        self.orders_url = '/api/orders/'
    
    def test_create_order_success(self):
        """测试创建订单成功"""
        data = {
            'shipping_address': '北京市朝阳区xxx街道',
            'contact_phone': '13800138000',
            'items': [
                {'product_name': '商品1', 'price': '99.00', 'quantity': 2},
                {'product_name': '商品2', 'price': '50.00', 'quantity': 1}
            ]
        }
        response = self.client.post(self.orders_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['code'], 201)
        self.assertIn('order_number', response.data['data'])
    
    def test_create_order_empty_items(self):
        """测试创建订单无商品"""
        data = {
            'shipping_address': '北京市',
            'contact_phone': '13800138000',
            'items': []
        }
        response = self.client.post(self.orders_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_order_missing_address(self):
        """测试创建订单缺少地址"""
        data = {
            'contact_phone': '13800138000',
            'items': [{'product_name': '商品', 'price': '99.00', 'quantity': 1}]
        }
        response = self.client.post(self.orders_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_orders(self):
        """测试获取订单列表"""
        # 创建测试订单
        Order.objects.create(
            user=self.user,
            shipping_address='地址1',
            contact_phone='13800138001'
        )
        Order.objects.create(
            user=self.user,
            shipping_address='地址2',
            contact_phone='13800138002'
        )
        
        response = self.client.get(self.orders_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_orders_only_own(self):
        """测试只能查看自己的订单"""
        # 创建自己的订单
        Order.objects.create(
            user=self.user,
            shipping_address='我的地址',
            contact_phone='13800138001'
        )
        # 创建其他用户的订单
        Order.objects.create(
            user=self.other_user,
            shipping_address='其他地址',
            contact_phone='13800138002'
        )
        
        response = self.client.get(self.orders_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 只能看到自己的订单
        orders = response.data.get('results', response.data.get('data', []))
        if isinstance(orders, list):
            self.assertEqual(len(orders), 1)
    
    def test_get_order_detail(self):
        """测试获取订单详情"""
        order = Order.objects.create(
            user=self.user,
            shipping_address='北京市',
            contact_phone='13800138000'
        )
        OrderItem.objects.create(
            order=order,
            product_name='测试商品',
            price=Decimal('99.00'),
            quantity=1
        )
        
        response = self.client.get(f'{self.orders_url}{order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 200)
        self.assertEqual(response.data['data']['order_number'], order.order_number)
    
    def test_get_other_user_order(self):
        """测试获取其他用户订单"""
        order = Order.objects.create(
            user=self.other_user,
            shipping_address='其他地址',
            contact_phone='13800138000'
        )
        
        response = self.client.get(f'{self.orders_url}{order.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_order(self):
        """测试更新订单"""
        order = Order.objects.create(
            user=self.user,
            shipping_address='旧地址',
            contact_phone='13800138000'
        )
        
        data = {
            'shipping_address': '新地址',
            'contact_phone': '13900139000'
        }
        response = self.client.put(f'{self.orders_url}{order.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        order.refresh_from_db()
        self.assertEqual(order.shipping_address, '新地址')
        self.assertEqual(order.contact_phone, '13900139000')
    
    def test_update_order_status(self):
        """测试更新订单状态"""
        order = Order.objects.create(
            user=self.user,
            shipping_address='北京市',
            contact_phone='13800138000'
        )
        
        response = self.client.patch(
            f'{self.orders_url}{order.id}/status/',
            {'status': 'processing'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        order.refresh_from_db()
        self.assertEqual(order.status, 'processing')
    
    def test_update_order_invalid_status(self):
        """测试更新无效订单状态"""
        order = Order.objects.create(
            user=self.user,
            shipping_address='北京市',
            contact_phone='13800138000'
        )
        
        response = self.client.patch(
            f'{self.orders_url}{order.id}/status/',
            {'status': 'invalid_status'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_order(self):
        """测试删除订单"""
        order = Order.objects.create(
            user=self.user,
            shipping_address='北京市',
            contact_phone='13800138000'
        )
        
        response = self.client.delete(f'{self.orders_url}{order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Order.objects.filter(id=order.id).exists())
    
    def test_delete_other_user_order(self):
        """测试删除其他用户订单"""
        order = Order.objects.create(
            user=self.other_user,
            shipping_address='其他地址',
            contact_phone='13800138000'
        )
        
        response = self.client.delete(f'{self.orders_url}{order.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrderFilterTestCase(APITestCase):
    """订单过滤测试"""
    
    def setUp(self):
        """测试前准备"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        self.orders_url = '/api/orders/'
        
        # 创建测试订单
        self.order1 = Order.objects.create(
            user=self.user,
            order_number='ORD001TEST',
            shipping_address='北京市',
            contact_phone='13800138001',
            status='pending'
        )
        self.order2 = Order.objects.create(
            user=self.user,
            order_number='ORD002TEST',
            shipping_address='上海市',
            contact_phone='13800138002',
            status='processing'
        )
        self.order3 = Order.objects.create(
            user=self.user,
            order_number='ORD003TEST',
            shipping_address='广州市',
            contact_phone='13800138003',
            status='delivered'
        )
    
    def test_filter_by_order_number(self):
        """测试按订单号过滤"""
        response = self.client.get(f'{self.orders_url}?order_number=ORD001')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filter_by_status(self):
        """测试按状态过滤"""
        response = self.client.get(f'{self.orders_url}?status=pending')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filter_by_keyword(self):
        """测试按关键词过滤"""
        response = self.client.get(f'{self.orders_url}?keyword=北京')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderItemAPITestCase(APITestCase):
    """订单项API测试"""
    
    def setUp(self):
        """测试前准备"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        
        self.order = Order.objects.create(
            user=self.user,
            shipping_address='北京市',
            contact_phone='13800138000'
        )
        self.item = OrderItem.objects.create(
            order=self.order,
            product_name='测试商品',
            price=Decimal('99.00'),
            quantity=1
        )
    
    def test_get_order_items(self):
        """测试获取订单项列表"""
        response = self.client.get(f'/api/orders/{self.order.id}/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 200)
    
    def test_add_order_item(self):
        """测试添加订单项"""
        data = {
            'product_name': '新商品',
            'price': '50.00',
            'quantity': 2
        }
        response = self.client.post(f'/api/orders/{self.order.id}/items/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.order.refresh_from_db()
        self.assertEqual(self.order.items.count(), 2)
    
    def test_delete_order_item(self):
        """测试删除订单项"""
        response = self.client.delete(
            f'/api/orders/{self.order.id}/items/{self.item.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(OrderItem.objects.filter(id=self.item.id).exists())


class UnauthorizedAccessTestCase(APITestCase):
    """未授权访问测试"""
    
    def test_list_orders_unauthorized(self):
        """测试未认证获取订单列表"""
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_order_unauthorized(self):
        """测试未认证创建订单"""
        data = {
            'shipping_address': '北京市',
            'contact_phone': '13800138000',
            'items': [{'product_name': '商品', 'price': '99.00', 'quantity': 1}]
        }
        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
