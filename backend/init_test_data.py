"""
初始化测试数据脚本
运行方式: python manage.py shell < init_test_data.py
或者: docker exec -i order_management_backend python manage.py shell < init_test_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User
from apps.orders.models import Order, OrderItem

# 创建管理员用户
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@example.com',
        'first_name': '管理员',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin_user.set_password('admin123')
    admin_user.save()
    print('Created admin user')
else:
    print('Admin user already exists')

# 测试订单数据
test_orders = [
    {
        'order_number': 'ORD20260101001',
        'total_amount': Decimal('1299.00'),
        'status': 'pending',
        'shipping_address': '北京市朝阳区建国路88号SOHO现代城A座1501室',
        'contact_phone': '13800138001',
        'items': [
            {'product_name': 'Apple AirPods Pro 2代', 'price': Decimal('1299.00'), 'quantity': 1},
        ]
    },
    {
        'order_number': 'ORD20260101002',
        'total_amount': Decimal('2599.00'),
        'status': 'processing',
        'shipping_address': '上海市浦东新区陆家嘴环路1000号恒生银行大厦25层',
        'contact_phone': '13900139002',
        'items': [
            {'product_name': 'Sony WH-1000XM5 头戴式耳机', 'price': Decimal('2299.00'), 'quantity': 1},
            {'product_name': '耳机收纳包', 'price': Decimal('150.00'), 'quantity': 2},
        ]
    },
    {
        'order_number': 'ORD20260101003',
        'total_amount': Decimal('899.00'),
        'status': 'shipped',
        'shipping_address': '广州市天河区珠江新城华夏路30号富力盈通大厦12楼',
        'contact_phone': '13700137003',
        'items': [
            {'product_name': '小米手环8 Pro', 'price': Decimal('299.00'), 'quantity': 1},
            {'product_name': '替换表带套装', 'price': Decimal('200.00'), 'quantity': 3},
        ]
    },
    {
        'order_number': 'ORD20260101004',
        'total_amount': Decimal('3999.00'),
        'status': 'delivered',
        'shipping_address': '深圳市南山区科技园南区高新南一道飞亚达大厦5层',
        'contact_phone': '13600136004',
        'items': [
            {'product_name': 'iPad Air 5 64GB', 'price': Decimal('3999.00'), 'quantity': 1},
        ]
    },
    {
        'order_number': 'ORD20260101005',
        'total_amount': Decimal('599.00'),
        'status': 'cancelled',
        'shipping_address': '杭州市西湖区文三路478号华星科技大厦8楼',
        'contact_phone': '13500135005',
        'items': [
            {'product_name': '罗技MX Master 3S鼠标', 'price': Decimal('599.00'), 'quantity': 1},
        ]
    },
    {
        'order_number': 'ORD20260101006',
        'total_amount': Decimal('1899.00'),
        'status': 'pending',
        'shipping_address': '成都市高新区天府大道北段1700号环球中心E1区12层',
        'contact_phone': '13400134006',
        'items': [
            {'product_name': 'Nintendo Switch OLED', 'price': Decimal('1599.00'), 'quantity': 1},
            {'product_name': '塞尔达传说：王国之泪', 'price': Decimal('300.00'), 'quantity': 1},
        ]
    },
    {
        'order_number': 'ORD20260101007',
        'total_amount': Decimal('4299.00'),
        'status': 'processing',
        'shipping_address': '武汉市江汉区建设大道568号新世界国贸大厦38层',
        'contact_phone': '13300133007',
        'items': [
            {'product_name': 'MacBook Air M2 256GB', 'price': Decimal('3999.00'), 'quantity': 1},
            {'product_name': 'Type-C扩展坞', 'price': Decimal('150.00'), 'quantity': 2},
        ]
    },
    {
        'order_number': 'ORD20260101008',
        'total_amount': Decimal('799.00'),
        'status': 'shipped',
        'shipping_address': '南京市鼓楼区中山北路30号城市名人酒店商务楼15层',
        'contact_phone': '13200132008',
        'items': [
            {'product_name': '飞利浦电动牙刷HX9352', 'price': Decimal('799.00'), 'quantity': 1},
        ]
    },
    {
        'order_number': 'ORD20260101009',
        'total_amount': Decimal('2199.00'),
        'status': 'delivered',
        'shipping_address': '西安市雁塔区高新路52号高新国际商务中心18层',
        'contact_phone': '13100131009',
        'items': [
            {'product_name': 'Bose SoundLink Flex 蓝牙音箱', 'price': Decimal('999.00'), 'quantity': 1},
            {'product_name': 'Bose 便携收纳袋', 'price': Decimal('200.00'), 'quantity': 1},
            {'product_name': '3.5mm音频线', 'price': Decimal('50.00'), 'quantity': 2},
            {'product_name': '车载充电器', 'price': Decimal('150.00'), 'quantity': 6},
        ]
    },
    {
        'order_number': 'ORD20260101010',
        'total_amount': Decimal('1599.00'),
        'status': 'pending',
        'shipping_address': '重庆市渝中区解放碑民权路28号英利国际金融中心22层',
        'contact_phone': '13000130010',
        'items': [
            {'product_name': 'Kindle Paperwhite 5', 'price': Decimal('999.00'), 'quantity': 1},
            {'product_name': 'Kindle保护套', 'price': Decimal('200.00'), 'quantity': 1},
            {'product_name': '屏幕保护膜', 'price': Decimal('50.00'), 'quantity': 2},
            {'product_name': 'Type-C充电线', 'price': Decimal('30.00'), 'quantity': 10},
        ]
    },
    {
        'order_number': 'ORD20260101011',
        'total_amount': Decimal('698.00'),
        'status': 'processing',
        'shipping_address': '天津市和平区南京路189号津汇广场1座20层',
        'contact_phone': '12900129011',
        'items': [
            {'product_name': '米家台灯Pro', 'price': Decimal('349.00'), 'quantity': 2},
        ]
    },
    {
        'order_number': 'ORD20260101012',
        'total_amount': Decimal('5999.00'),
        'status': 'shipped',
        'shipping_address': '苏州市工业园区苏州大道东265号现代传媒广场16层',
        'contact_phone': '12800128012',
        'items': [
            {'product_name': 'DJI Mini 3 Pro 无人机', 'price': Decimal('4999.00'), 'quantity': 1},
            {'product_name': '无人机电池', 'price': Decimal('500.00'), 'quantity': 2},
        ]
    },
]

# 插入订单数据
created_count = 0
for order_data in test_orders:
    if not Order.objects.filter(order_number=order_data['order_number']).exists():
        items_data = order_data.pop('items')
        order = Order.objects.create(user=admin_user, **order_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        created_count += 1
        print(f"Created order: {order.order_number}")

print(f"\nTotal: {created_count} orders created")
print(f"Total orders in database: {Order.objects.count()}")
