"""
订单模块视图
"""
import logging
from datetime import datetime, timedelta
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Sum
from django.db.models.functions import TruncMonth
from .models import Order, OrderItem
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderUpdateSerializer,
    OrderStatusUpdateSerializer,
    OrderItemSerializer,
    OrderItemCreateSerializer
)

logger = logging.getLogger('apps')


class OrderViewSet(viewsets.ModelViewSet):
    """
    订单视图集
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """获取当前用户的订单列表，支持搜索过滤"""
        queryset = Order.objects.filter(user=self.request.user)
        
        # 订单号搜索
        order_number = self.request.query_params.get('order_number')
        if order_number:
            queryset = queryset.filter(order_number__icontains=order_number)
        
        # 状态过滤
        order_status = self.request.query_params.get('status')
        if order_status:
            queryset = queryset.filter(status=order_status)
        
        # 日期范围过滤
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        
        # 关键词搜索（搜索订单号、收货地址、联系电话）
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(order_number__icontains=keyword) |
                Q(shipping_address__icontains=keyword) |
                Q(contact_phone__icontains=keyword)
            )
        
        return queryset
    
    def get_serializer_class(self):
        """根据操作选择序列化器"""
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderSerializer
    
    def list(self, request, *args, **kwargs):
        """
        获取订单列表（分页）
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # 自定义分页响应格式
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': {
                    'results': serializer.data,
                    'count': self.paginator.page.paginator.count
                }
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        """
        创建订单
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            logger.info(f"User {request.user.username} created order {order.order_number}")
            return Response({
                'code': 201,
                'message': '订单创建成功',
                'data': OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'code': 400,
            'message': '订单创建失败',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        """
        获取订单详情
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        """
        更新订单
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User {request.user.username} updated order {instance.order_number}")
            return Response({
                'code': 200,
                'message': '订单更新成功',
                'data': OrderSerializer(instance).data
            })
        
        return Response({
            'code': 400,
            'message': '订单更新失败',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        """
        部分更新订单
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User {request.user.username} partially updated order {instance.order_number}")
            return Response({
                'code': 200,
                'message': '订单更新成功',
                'data': OrderSerializer(instance).data
            })
        
        return Response({
            'code': 400,
            'message': '订单更新失败',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """
        删除订单
        """
        instance = self.get_object()
        order_number = instance.order_number
        instance.delete()
        logger.info(f"User {request.user.username} deleted order {order_number}")
        return Response({
            'code': 200,
            'message': '订单删除成功',
            'data': None
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        """
        更新订单状态
        """
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            old_status = order.status
            order.status = serializer.validated_data['status']
            order.save()
            logger.info(
                f"User {request.user.username} changed order {order.order_number} "
                f"status from {old_status} to {order.status}"
            )
            return Response({
                'code': 200,
                'message': '订单状态更新成功',
                'data': OrderSerializer(order).data
            })
        
        return Response({
            'code': 400,
            'message': '订单状态更新失败',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get', 'post'])
    def items(self, request, pk=None):
        """
        订单项管理
        """
        order = self.get_object()
        
        if request.method == 'GET':
            # 获取订单项列表
            items = order.items.all()
            serializer = OrderItemSerializer(items, many=True)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        
        elif request.method == 'POST':
            # 添加订单项
            serializer = OrderItemCreateSerializer(data=request.data)
            if serializer.is_valid():
                item = serializer.save(order=order)
                logger.info(
                    f"User {request.user.username} added item to order {order.order_number}"
                )
                return Response({
                    'code': 201,
                    'message': '订单项添加成功',
                    'data': OrderItemSerializer(item).data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'code': 400,
                'message': '订单项添加失败',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='items/(?P<item_id>[^/.]+)')
    def delete_item(self, request, pk=None, item_id=None):
        """
        删除订单项
        """
        order = self.get_object()
        item = get_object_or_404(OrderItem, id=item_id, order=order)
        item.delete()
        logger.info(
            f"User {request.user.username} deleted item from order {order.order_number}"
        )
        return Response({
            'code': 200,
            'message': '订单项删除成功',
            'data': None
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        订单统计接口
        支持按时间范围筛选：本周/本月/自定义区间
        """
        queryset = Order.objects.filter(user=request.user)
        
        time_range = request.query_params.get('time_range', 'all')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        today = datetime.now().date()
        
        if time_range == 'week':
            start_date = today - timedelta(days=today.weekday())
            end_date = today
        elif time_range == 'month':
            start_date = today.replace(day=1)
            end_date = today
        elif time_range == 'custom' and start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({
                    'code': 400,
                    'message': '日期格式错误，请使用 YYYY-MM-DD 格式',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if start_date and end_date:
            queryset = queryset.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)
        
        status_stats = queryset.values('status').annotate(count=Count('id')).order_by('status')
        status_map = {choice[0]: choice[1] for choice in Order.STATUS_CHOICES}
        status_data = []
        for stat in status_stats:
            status_data.append({
                'status': stat['status'],
                'status_display': status_map.get(stat['status'], stat['status']),
                'count': stat['count']
            })
        
        monthly_trend = queryset.annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            total_amount=Sum('total_amount'),
            order_count=Count('id')
        ).order_by('month')
        
        monthly_data = []
        for item in monthly_trend:
            monthly_data.append({
                'month': item['month'].strftime('%Y-%m') if item['month'] else None,
                'total_amount': float(item['total_amount']) if item['total_amount'] else 0,
                'order_count': item['order_count']
            })
        
        source_stats = queryset.values('status').annotate(count=Count('id')).order_by('-count')
        source_data = []
        total_orders = queryset.count()
        for stat in source_stats:
            percentage = round((stat['count'] / total_orders * 100), 1) if total_orders > 0 else 0
            source_data.append({
                'name': status_map.get(stat['status'], stat['status']),
                'value': stat['count'],
                'percentage': percentage
            })
        
        summary = {
            'total_orders': total_orders,
            'total_amount': float(queryset.aggregate(Sum('total_amount'))['total_amount__sum'] or 0),
            'pending_count': queryset.filter(status='pending').count(),
            'completed_count': queryset.filter(status='delivered').count()
        }
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'summary': summary,
                'status_stats': status_data,
                'monthly_trend': monthly_data,
                'source_distribution': source_data
            }
        })
