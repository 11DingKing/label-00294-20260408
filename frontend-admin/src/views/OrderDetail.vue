<template>
  <div class="page-container">
    <div class="page-header">
      <el-button @click="router.back()" class="back-btn">
        <el-icon><ArrowLeft /></el-icon>
        返回列表
      </el-button>
    </div>
    
    <div v-loading="loading" class="detail-content">
      <template v-if="order">
        <!-- 订单头部信息 -->
        <div class="order-header card-container">
          <div class="header-main">
            <div class="order-info">
              <h1 class="order-number">{{ order.order_number }}</h1>
              <el-tag :class="['status-tag', `status-${order.status}`]" size="large">
                {{ order.status_display }}
              </el-tag>
            </div>
            <div class="order-amount">
              <span class="label">订单金额</span>
              <span class="value">¥{{ parseFloat(order.total_amount).toFixed(2) }}</span>
            </div>
          </div>
          <div class="header-actions">
            <el-button type="primary" @click="showStatusDialog = true">
              <el-icon><Edit /></el-icon>
              更新状态
            </el-button>
            <el-button @click="showEditDialog = true">
              <el-icon><EditPen /></el-icon>
              编辑信息
            </el-button>
            <el-button type="danger" @click="handleDelete">
              <el-icon><Delete /></el-icon>
              删除订单
            </el-button>
          </div>
        </div>
        
        <div class="detail-grid">
          <!-- 基本信息 -->
          <div class="card-container info-card">
            <h3 class="card-title">
              <el-icon><User /></el-icon>
              收货信息
            </h3>
            <div class="info-list">
              <div class="info-item">
                <span class="info-label">联系电话</span>
                <span class="info-value">{{ order.contact_phone }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">收货地址</span>
                <span class="info-value">{{ order.shipping_address }}</span>
              </div>
            </div>
          </div>
          
          <!-- 时间信息 -->
          <div class="card-container info-card">
            <h3 class="card-title">
              <el-icon><Clock /></el-icon>
              时间信息
            </h3>
            <div class="info-list">
              <div class="info-item">
                <span class="info-label">创建时间</span>
                <span class="info-value">{{ formatTime(order.created_at) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">更新时间</span>
                <span class="info-value">{{ formatTime(order.updated_at) }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 订单项列表 -->
        <div class="card-container">
          <h3 class="card-title">
            <el-icon><ShoppingCart /></el-icon>
            商品明细
            <span class="item-count">{{ order.items?.length || 0 }} 件商品</span>
          </h3>
          
          <el-table :data="order.items" class="items-table">
            <el-table-column prop="product_name" label="商品名称" min-width="200">
              <template #default="{ row }">
                <div class="product-name">
                  <el-icon class="product-icon"><Box /></el-icon>
                  {{ row.product_name }}
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="price" label="单价" width="140" align="right">
              <template #default="{ row }">
                <span class="price">¥{{ parseFloat(row.price).toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" width="100" align="center">
              <template #default="{ row }">
                <span class="quantity">×{{ row.quantity }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="subtotal" label="小计" width="140" align="right">
              <template #default="{ row }">
                <span class="subtotal">¥{{ parseFloat(row.subtotal).toFixed(2) }}</span>
              </template>
            </el-table-column>
          </el-table>
          
          <div class="order-summary">
            <div class="summary-row">
              <span>商品总数</span>
              <span>{{ totalQuantity }} 件</span>
            </div>
            <div class="summary-row total">
              <span>订单总额</span>
              <span class="total-amount">¥{{ parseFloat(order.total_amount).toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </template>
    </div>
    
    <!-- 编辑对话框 -->
    <el-dialog v-model="showEditDialog" title="编辑订单信息" width="500px">
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editRules"
        label-position="top"
      >
        <el-form-item label="收货地址" prop="shipping_address">
          <el-input
            v-model="editForm.shipping_address"
            type="textarea"
            :rows="3"
            placeholder="请输入收货地址"
          />
        </el-form-item>
        <el-form-item label="联系电话" prop="contact_phone">
          <el-input v-model="editForm.contact_phone" placeholder="请输入联系电话" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" :loading="updating" @click="handleUpdate">
          保存修改
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 状态更新对话框 -->
    <el-dialog v-model="showStatusDialog" title="更新订单状态" width="420px">
      <div class="status-options">
        <div
          v-for="status in statusOptions"
          :key="status.value"
          class="status-option"
          :class="{ active: statusForm.status === status.value }"
          @click="statusForm.status = status.value"
        >
          <el-icon :class="['status-icon', `icon-${status.value}`]">
            <component :is="status.icon" />
          </el-icon>
          <span>{{ status.label }}</span>
        </div>
      </div>
      <template #footer>
        <el-button @click="showStatusDialog = false">取消</el-button>
        <el-button type="primary" :loading="updating" @click="handleStatusUpdate">
          确认更新
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useOrderStore } from '@/store/orders'
import { ElMessageBox } from 'element-plus'
import { toast, notify } from '@/utils/toast'
import { 
  ArrowLeft, Edit, EditPen, Delete, User, Clock, 
  ShoppingCart, Box, CircleCheck, Loading, Van, Close
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const orderStore = useOrderStore()

const loading = ref(false)
const updating = ref(false)
const showEditDialog = ref(false)
const showStatusDialog = ref(false)

const order = computed(() => orderStore.currentOrder)

const totalQuantity = computed(() => {
  return order.value?.items?.reduce((sum, item) => sum + item.quantity, 0) || 0
})

const editForm = reactive({
  shipping_address: '',
  contact_phone: ''
})

const statusForm = reactive({
  status: ''
})

const editFormRef = ref(null)

const editRules = {
  shipping_address: [
    { required: true, message: '请输入收货地址', trigger: 'blur' }
  ],
  contact_phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' }
  ]
}

const statusOptions = [
  { value: 'pending', label: '待处理', icon: Clock },
  { value: 'processing', label: '处理中', icon: Loading },
  { value: 'shipped', label: '已发货', icon: Van },
  { value: 'delivered', label: '已送达', icon: CircleCheck },
  { value: 'cancelled', label: '已取消', icon: Close }
]

const formatTime = (time) => {
  if (!time) return '-'
  return time.replace('T', ' ').substring(0, 19)
}

const loadOrder = async () => {
  loading.value = true
  try {
    await orderStore.fetchOrderDetail(route.params.id)
    if (order.value) {
      editForm.shipping_address = order.value.shipping_address
      editForm.contact_phone = order.value.contact_phone
      statusForm.status = order.value.status
    }
  } catch (error) {
    toast.error('加载订单详情失败')
  } finally {
    loading.value = false
  }
}

const handleUpdate = async () => {
  if (!editFormRef.value) return
  
  await editFormRef.value.validate(async (valid) => {
    if (valid) {
      updating.value = true
      try {
        await orderStore.updateOrder(route.params.id, editForm)
        showEditDialog.value = false
        notify.success('保存成功', '订单信息已更新')
        await loadOrder()
      } catch (error) {
        toast.error('保存失败')
      } finally {
        updating.value = false
      }
    }
  })
}

const handleStatusUpdate = async () => {
  if (!statusForm.status) {
    toast.warning('请选择订单状态')
    return
  }
  
  updating.value = true
  try {
    await orderStore.changeOrderStatus(route.params.id, statusForm.status)
    showStatusDialog.value = false
    notify.success('状态更新成功', '订单状态已更新')
    await loadOrder()
  } catch (error) {
    toast.error('状态更新失败')
  } finally {
    updating.value = false
  }
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除订单 ${order.value?.order_number} 吗？此操作不可恢复！`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    await orderStore.removeOrder(route.params.id)
    notify.success('删除成功', `订单 ${order.value?.order_number} 已删除`)
    router.push('/orders')
  } catch (error) {
    if (error !== 'cancel') {
      toast.error('删除失败')
    }
  }
}

onMounted(() => {
  loadOrder()
})
</script>

<style scoped lang="scss">
.page-header {
  margin-bottom: 24px;
  
  .back-btn {
    font-weight: 500;
  }
}

.order-header {
  .header-main {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
    
    .order-info {
      display: flex;
      align-items: center;
      gap: 16px;
      
      .order-number {
        font-size: 24px;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
        font-family: 'SF Mono', 'Monaco', monospace;
      }
      
      .status-tag {
        border-radius: 20px;
        padding: 6px 16px;
        font-weight: 600;
        
        &.status-pending { background: #fef3c7; color: #d97706; }
        &.status-processing { background: #dbeafe; color: #2563eb; }
        &.status-shipped { background: #e0e7ff; color: #4f46e5; }
        &.status-delivered { background: #d1fae5; color: #059669; }
        &.status-cancelled { background: #fee2e2; color: #dc2626; }
      }
    }
    
    .order-amount {
      text-align: right;
      
      .label {
        display: block;
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 4px;
      }
      
      .value {
        font-size: 32px;
        font-weight: 700;
        color: #ef4444;
      }
    }
  }
  
  .header-actions {
    display: flex;
    gap: 16px;
    padding-top: 20px;
    border-top: 1px solid #e5e7eb;
  }
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

.info-card {
  .card-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
    color: #1f2937;
    margin: 0 0 20px 0;
    
    .el-icon {
      color: #6366f1;
    }
  }
  
  .info-list {
    .info-item {
      display: flex;
      justify-content: space-between;
      padding: 12px 0;
      border-bottom: 1px solid #f3f4f6;
      
      &:last-child {
        border-bottom: none;
      }
      
      .info-label {
        color: #6b7280;
        font-size: 14px;
      }
      
      .info-value {
        color: #1f2937;
        font-weight: 500;
        text-align: right;
        max-width: 60%;
      }
    }
  }
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 20px 0;
  
  .el-icon {
    color: #6366f1;
  }
  
  .item-count {
    margin-left: auto;
    font-size: 14px;
    font-weight: 400;
    color: #6b7280;
  }
}

.items-table {
  .product-name {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .product-icon {
      color: #6366f1;
    }
  }
  
  .price {
    color: #374151;
  }
  
  .quantity {
    color: #6b7280;
    font-weight: 500;
  }
  
  .subtotal {
    font-weight: 600;
    color: #1f2937;
  }
}

.order-summary {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
  
  .summary-row {
    display: flex;
    justify-content: flex-end;
    gap: 40px;
    padding: 8px 0;
    font-size: 14px;
    color: #6b7280;
    
    &.total {
      font-size: 16px;
      font-weight: 600;
      color: #1f2937;
      padding-top: 12px;
      
      .total-amount {
        font-size: 24px;
        color: #ef4444;
      }
    }
  }
}

.status-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  
  .status-option {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 16px;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    
    &:hover {
      border-color: #6366f1;
      background: #f5f3ff;
    }
    
    &.active {
      border-color: #6366f1;
      background: #f5f3ff;
    }
    
    .status-icon {
      font-size: 24px;
      
      &.icon-pending { color: #d97706; }
      &.icon-processing { color: #2563eb; }
      &.icon-shipped { color: #4f46e5; }
      &.icon-delivered { color: #059669; }
      &.icon-cancelled { color: #dc2626; }
    }
    
    span {
      font-size: 13px;
      font-weight: 500;
      color: #374151;
    }
  }
}
</style>
