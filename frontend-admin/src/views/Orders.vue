<template>
  <div class="page-container">
    <!-- 统计卡片 -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-icon pending">
          <el-icon><Clock /></el-icon>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ stats.pending }}</span>
          <span class="stat-label">待处理</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon processing">
          <el-icon><Loading /></el-icon>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ stats.processing }}</span>
          <span class="stat-label">处理中</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon shipped">
          <el-icon><Van /></el-icon>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ stats.shipped }}</span>
          <span class="stat-label">已发货</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon delivered">
          <el-icon><CircleCheck /></el-icon>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ stats.delivered }}</span>
          <span class="stat-label">已完成</span>
        </div>
      </div>
    </div>

    <div class="card-container">
      <!-- 工具栏 -->
      <div class="toolbar">
        <div class="toolbar-left">
          <el-input
            v-model="searchForm.order_number"
            placeholder="搜索订单号..."
            clearable
            class="search-input"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          
          <el-select
            v-model="searchForm.status"
            placeholder="订单状态"
            clearable
            class="filter-select"
          >
            <el-option label="待处理" value="pending" />
            <el-option label="处理中" value="processing" />
            <el-option label="已发货" value="shipped" />
            <el-option label="已送达" value="delivered" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
          
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            class="date-picker"
          />
          
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </div>
        
        <div class="toolbar-right">
          <el-button type="success" @click="handleExport">
            <el-icon><Download /></el-icon>
            导出
          </el-button>
          <el-button type="primary" @click="showCreateDialog = true">
            <el-icon><Plus /></el-icon>
            新建订单
          </el-button>
        </div>
      </div>

      <!-- 订单表格 -->
      <el-table
        v-loading="orderStore.loading"
        :data="orderStore.orders"
        class="order-table"
        :row-class-name="tableRowClassName"
      >
        <el-table-column prop="order_number" label="订单号" width="180">
          <template #default="{ row }">
            <span class="order-number" @click="handleView(row.id)">
              {{ row.order_number }}
            </span>
          </template>
        </el-table-column>
        
        <el-table-column prop="total_amount" label="订单金额" width="140" align="right">
          <template #default="{ row }">
            <span class="amount">¥{{ parseFloat(row.total_amount).toFixed(2) }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="120" align="center">
          <template #default="{ row }">
            <el-tag :class="['status-tag', `status-${row.status}`]" effect="light">
              {{ row.status_display }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="contact_phone" label="联系电话" width="140" />
        
        <el-table-column prop="shipping_address" label="收货地址" min-width="200" show-overflow-tooltip />
        
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            <span class="time-text">{{ formatTime(row.created_at) }}</span>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" fixed="right" width="180" align="center">
          <template #default="{ row }">
            <div class="action-buttons">
              <span class="action-link primary" @click="handleView(row.id)">查看</span>
              <span class="action-link warning" @click="handleStatusChange(row)">状态</span>
              <span class="action-link danger" @click="handleDelete(row)">删除</span>
            </div>
          </template>
        </el-table-column>
        
        <template #empty>
          <div class="empty-state">
            <el-icon :size="48"><Document /></el-icon>
            <p>暂无订单数据</p>
          </div>
        </template>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <span class="total-text">共 {{ orderStore.total }} 条记录</span>
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :total="orderStore.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>
    
    <!-- 状态更新对话框 -->
    <el-dialog v-model="showStatusDialog" title="更新订单状态" width="400px">
      <div class="status-options">
        <div
          v-for="status in statusOptions"
          :key="status.value"
          class="status-option"
          :class="{ active: selectedStatus === status.value }"
          @click="selectedStatus = status.value"
        >
          <el-icon :class="['status-icon', `icon-${status.value}`]">
            <component :is="status.icon" />
          </el-icon>
          <span>{{ status.label }}</span>
        </div>
      </div>
      <template #footer>
        <el-button @click="showStatusDialog = false">取消</el-button>
        <el-button type="primary" :loading="statusLoading" @click="confirmStatusChange">
          确认更新
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 新建订单对话框 -->
    <el-dialog 
      v-model="showCreateDialog" 
      title="新建订单" 
      width="700px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="createFormRef"
        :model="createForm"
        :rules="createRules"
        label-position="top"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系电话" prop="contact_phone">
              <el-input
                v-model="createForm.contact_phone"
                placeholder="请输入联系电话"
              >
                <template #prefix>
                  <el-icon><Phone /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="收货地址" prop="shipping_address">
          <el-input
            v-model="createForm.shipping_address"
            type="textarea"
            :rows="2"
            placeholder="请输入详细收货地址"
          />
        </el-form-item>
        
        <el-form-item label="商品信息">
          <div class="items-list">
            <div
              v-for="(item, index) in createForm.items"
              :key="index"
              class="item-row"
            >
              <span class="item-index">{{ index + 1 }}</span>
              <el-input
                v-model="item.product_name"
                placeholder="商品名称"
                style="flex: 1"
              />
              <el-input-number
                v-model="item.price"
                :min="0.01"
                :precision="2"
                :controls="false"
                placeholder="单价"
                style="width: 120px"
              />
              <el-input-number
                v-model="item.quantity"
                :min="1"
                placeholder="数量"
                style="width: 100px"
              />
              <span class="item-subtotal">¥{{ (item.price * item.quantity || 0).toFixed(2) }}</span>
              <el-button
                type="danger"
                :icon="Delete"
                circle
                size="small"
                @click="removeCreateItem(index)"
                :disabled="createForm.items.length <= 1"
              />
            </div>
          </div>
          <el-button type="primary" @click="addCreateItem">
            <el-icon><Plus /></el-icon>
            添加商品
          </el-button>
        </el-form-item>
        
        <div class="create-summary">
          <span>订单总额：</span>
          <span class="total-amount">¥{{ createTotalAmount.toFixed(2) }}</span>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" :loading="createLoading" @click="handleCreateSubmit">
          提交订单
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useOrderStore } from '@/store/orders'
import { ElMessageBox } from 'element-plus'
import { toast, notify } from '@/utils/toast'
import { 
  Plus, View, Edit, Delete, Download, Search, Refresh,
  Clock, Loading, Van, CircleCheck, Document, Close, Phone
} from '@element-plus/icons-vue'

const router = useRouter()
const orderStore = useOrderStore()

const searchForm = reactive({
  order_number: '',
  status: '',
  dateRange: null
})

const pagination = reactive({
  page: 1,
  size: 10
})

// 统计数据
const stats = computed(() => {
  const orders = orderStore.orders || []
  return {
    pending: orders.filter(o => o.status === 'pending').length,
    processing: orders.filter(o => o.status === 'processing').length,
    shipped: orders.filter(o => o.status === 'shipped').length,
    delivered: orders.filter(o => o.status === 'delivered').length
  }
})

// 状态更新
const showStatusDialog = ref(false)
const statusLoading = ref(false)
const selectedStatus = ref('')
const currentOrder = ref(null)

// 新建订单
const showCreateDialog = ref(false)
const createLoading = ref(false)
const createFormRef = ref(null)
const createForm = reactive({
  shipping_address: '',
  contact_phone: '',
  items: [{ product_name: '', price: 0, quantity: 1 }]
})

const createRules = {
  shipping_address: [{ required: true, message: '请输入收货地址', trigger: 'blur' }],
  contact_phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

const createTotalAmount = computed(() => {
  return createForm.items.reduce((sum, item) => sum + (item.price || 0) * (item.quantity || 0), 0)
})

const addCreateItem = () => {
  createForm.items.push({ product_name: '', price: 0, quantity: 1 })
}

const removeCreateItem = (index) => {
  if (createForm.items.length > 1) {
    createForm.items.splice(index, 1)
  }
}

const resetCreateForm = () => {
  createForm.shipping_address = ''
  createForm.contact_phone = ''
  createForm.items = [{ product_name: '', price: 0, quantity: 1 }]
}

const handleCreateSubmit = async () => {
  if (!createFormRef.value) return
  
  await createFormRef.value.validate(async (valid) => {
    if (valid) {
      const hasInvalidItem = createForm.items.some(
        item => !item.product_name || item.price <= 0 || item.quantity <= 0
      )
      if (hasInvalidItem) {
        toast.warning('请完善商品信息')
        return
      }
      
      createLoading.value = true
      try {
        const order = await orderStore.createOrder(createForm)
        showCreateDialog.value = false
        resetCreateForm()
        notify.success('创建成功', `订单 ${order.order_number} 已创建`)
        loadOrders()
      } catch (error) {
        toast.error(error.message || '订单创建失败')
      } finally {
        createLoading.value = false
      }
    }
  })
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
  return time.replace('T', ' ').substring(0, 16)
}

const tableRowClassName = ({ row }) => {
  if (row.status === 'cancelled') return 'row-cancelled'
  return ''
}

const loadOrders = async () => {
  const params = {
    page: pagination.page,
    page_size: pagination.size
  }
  if (searchForm.order_number) {
    params.order_number = searchForm.order_number
  }
  if (searchForm.status) {
    params.status = searchForm.status
  }
  if (searchForm.dateRange && searchForm.dateRange.length === 2) {
    params.start_date = searchForm.dateRange[0]
    params.end_date = searchForm.dateRange[1]
  }
  try {
    await orderStore.fetchOrders(params)
  } catch (error) {
    toast.error('加载订单列表失败')
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadOrders()
  toast.success('查询完成')
}

const handleReset = () => {
  searchForm.order_number = ''
  searchForm.status = ''
  searchForm.dateRange = null
  pagination.page = 1
  loadOrders()
  toast.info('已重置筛选条件')
}

const handleView = (id) => {
  router.push(`/orders/${id}`)
}

const handleStatusChange = (row) => {
  currentOrder.value = row
  selectedStatus.value = row.status
  showStatusDialog.value = true
}

const confirmStatusChange = async () => {
  if (!selectedStatus.value || !currentOrder.value) return
  
  statusLoading.value = true
  try {
    await orderStore.changeOrderStatus(currentOrder.value.id, selectedStatus.value)
    showStatusDialog.value = false
    notify.success('状态更新成功', `订单 ${currentOrder.value.order_number} 状态已更新`)
    loadOrders()
  } catch (error) {
    toast.error('状态更新失败')
  } finally {
    statusLoading.value = false
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除订单 ${row.order_number} 吗？此操作不可恢复！`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    await orderStore.removeOrder(row.id)
    notify.success('删除成功', `订单 ${row.order_number} 已删除`)
    loadOrders()
  } catch (error) {
    if (error !== 'cancel') {
      toast.error('删除失败')
    }
  }
}

const handleExport = () => {
  const orders = orderStore.orders
  if (!orders || orders.length === 0) {
    toast.warning('暂无数据可导出')
    return
  }
  
  const statusMap = {
    pending: '待处理',
    processing: '处理中',
    shipped: '已发货',
    delivered: '已送达',
    cancelled: '已取消'
  }
  
  const headers = ['订单号', '订单金额', '状态', '联系电话', '收货地址', '创建时间']
  const rows = orders.map(order => [
    order.order_number,
    order.total_amount,
    statusMap[order.status] || order.status,
    order.contact_phone,
    `"${order.shipping_address.replace(/"/g, '""')}"`,
    order.created_at
  ])
  
  const csvContent = '\uFEFF' + [headers.join(','), ...rows.map(row => row.join(','))].join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `订单列表_${new Date().toISOString().slice(0, 10)}.csv`
  link.click()
  URL.revokeObjectURL(link.href)
  
  notify.success('导出成功', `已导出 ${orders.length} 条订单记录`)
}

const handleSizeChange = () => loadOrders()
const handlePageChange = () => loadOrders()

onMounted(() => {
  loadOrders()
})
</script>

<style scoped lang="scss">
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
  
  .stat-icon {
    width: 56px;
    height: 56px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    
    &.pending {
      background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
      color: #d97706;
    }
    
    &.processing {
      background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
      color: #2563eb;
    }
    
    &.shipped {
      background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
      color: #4f46e5;
    }
    
    &.delivered {
      background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
      color: #059669;
    }
  }
  
  .stat-content {
    display: flex;
    flex-direction: column;
    
    .stat-value {
      font-size: 28px;
      font-weight: 700;
      color: #1f2937;
      line-height: 1;
    }
    
    .stat-label {
      font-size: 14px;
      color: #6b7280;
      margin-top: 4px;
    }
  }
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 12px;
  
  .toolbar-left {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }
  
  .toolbar-right {
    display: flex;
    gap: 12px;
  }
  
  .search-input {
    width: 220px;
  }
  
  .filter-select {
    width: 140px;
  }
  
  .date-picker {
    width: 260px;
  }
}

.order-table {
  :deep(.el-table__header) {
    th {
      background: #f9fafb !important;
      font-weight: 600;
      color: #6b7280;
      font-size: 13px;
    }
  }
  
  :deep(.row-cancelled) {
    opacity: 0.6;
  }
  
  .order-number {
    font-family: 'SF Mono', 'Monaco', monospace;
    font-weight: 600;
    color: #6366f1;
    cursor: pointer;
    
    &:hover {
      text-decoration: underline;
    }
  }
  
  .amount {
    font-weight: 700;
    color: #ef4444;
    font-size: 15px;
  }
  
  .status-tag {
    border-radius: 20px;
    padding: 4px 12px;
    font-weight: 500;
    
    &.status-pending {
      background: #fef3c7;
      color: #d97706;
    }
    
    &.status-processing {
      background: #dbeafe;
      color: #2563eb;
    }
    
    &.status-shipped {
      background: #e0e7ff;
      color: #4f46e5;
    }
    
    &.status-delivered {
      background: #d1fae5;
      color: #059669;
    }
    
    &.status-cancelled {
      background: #fee2e2;
      color: #dc2626;
    }
  }
  
  .time-text {
    color: #6b7280;
    font-size: 13px;
  }
  
  .action-buttons {
    display: flex;
    justify-content: center;
    gap: 16px;
    
    .action-link {
      cursor: pointer;
      font-size: 14px;
      transition: opacity 0.2s;
      
      &:hover {
        opacity: 0.7;
      }
      
      &.primary {
        color: #6366f1;
      }
      
      &.warning {
        color: #f59e0b;
      }
      
      &.danger {
        color: #ef4444;
      }
    }
  }
}

.empty-state {
  padding: 60px 20px;
  text-align: center;
  color: #9ca3af;
  
  .el-icon {
    margin-bottom: 16px;
  }
  
  p {
    margin-bottom: 20px;
    font-size: 15px;
  }
}

.pagination-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
  
  .total-text {
    color: #6b7280;
    font-size: 14px;
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

.items-list {
  .item-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 16px;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    margin-bottom: 12px;
    transition: all 0.2s ease;
    
    &:hover {
      border-color: #6366f1;
      box-shadow: 0 2px 8px rgba(99, 102, 241, 0.1);
    }
    
    .item-index {
      width: 28px;
      height: 28px;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      color: white;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 600;
      flex-shrink: 0;
    }
    
    .item-subtotal {
      min-width: 90px;
      text-align: right;
      font-weight: 700;
      color: #ef4444;
      font-size: 15px;
    }
    
    :deep(.el-input__wrapper),
    :deep(.el-input-number .el-input__wrapper) {
      background: #f9fafb !important;
      border: 1px solid #e5e7eb !important;
      box-shadow: none !important;
      
      &:hover {
        border-color: #d1d5db !important;
      }
      
      &.is-focus {
        border-color: #6366f1 !important;
        background: #fff !important;
      }
    }
  }
}

.create-summary {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background: #ffffff;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  margin-top: 20px;
  
  span:first-child {
    font-size: 15px;
    color: #6b7280;
    font-weight: 500;
  }
  
  .total-amount {
    font-size: 28px;
    font-weight: 700;
    color: #1f2937;
  }
}


</style>
