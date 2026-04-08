"""
订单模块模型
"""
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Order(models.Model):
    """订单模型"""
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('cancelled', '已取消'),
    ]
    
    order_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name='订单号'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='用户'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='订单总额'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='订单状态'
    )
    shipping_address = models.TextField(
        verbose_name='收货地址'
    )
    contact_phone = models.CharField(
        max_length=20,
        verbose_name='联系电话'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        db_table = 'orders'
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.order_number} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_order_number():
        """生成唯一订单号"""
        return f"ORD{uuid.uuid4().hex[:12].upper()}"


class OrderItem(models.Model):
    """订单项模型"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='订单'
    )
    product_name = models.CharField(
        max_length=200,
        verbose_name='商品名称'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='单价'
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='数量'
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='小计'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    class Meta:
        db_table = 'order_items'
        verbose_name = '订单项'
        verbose_name_plural = '订单项'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order.order_number} - {self.product_name}"
    
    def save(self, *args, **kwargs):
        # 自动计算小计
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)
        
        # 更新订单总额
        self.order.total_amount = sum(item.subtotal for item in self.order.items.all())
        self.order.save(update_fields=['total_amount'])
