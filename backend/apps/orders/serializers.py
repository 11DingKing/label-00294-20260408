"""
订单模块序列化器
"""
from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """订单项序列化器"""
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'price', 'quantity', 'subtotal', 'created_at']
        read_only_fields = ['id', 'subtotal', 'created_at']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """订单项创建序列化器"""
    class Meta:
        model = OrderItem
        fields = ['product_name', 'price', 'quantity']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('单价必须大于0')
        return value
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('数量必须大于0')
        return value


class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器"""
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'total_amount', 'status',
            'status_display', 'shipping_address', 'contact_phone',
            'created_at', 'updated_at', 'items'
        ]
        read_only_fields = ['id', 'order_number', 'user', 'total_amount', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """订单创建序列化器"""
    items = OrderItemCreateSerializer(many=True, write_only=True)
    
    class Meta:
        model = Order
        fields = ['shipping_address', 'contact_phone', 'items']
    
    def validate_shipping_address(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('收货地址不能为空')
        return value.strip()
    
    def validate_contact_phone(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('联系电话不能为空')
        return value.strip()
    
    def validate_items(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError('订单必须包含至少一个商品')
        return value
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # 计算订单总额
        total_amount = sum(
            item['price'] * item['quantity'] for item in items_data
        )
        
        order = Order.objects.create(
            user=self.context['request'].user,
            total_amount=total_amount,
            **validated_data
        )
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    """订单更新序列化器"""
    class Meta:
        model = Order
        fields = ['shipping_address', 'contact_phone']
    
    def validate_shipping_address(self, value):
        if value and not value.strip():
            raise serializers.ValidationError('收货地址不能为空')
        return value.strip() if value else value
    
    def validate_contact_phone(self, value):
        if value and not value.strip():
            raise serializers.ValidationError('联系电话不能为空')
        return value.strip() if value else value


class OrderStatusUpdateSerializer(serializers.Serializer):
    """订单状态更新序列化器"""
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
