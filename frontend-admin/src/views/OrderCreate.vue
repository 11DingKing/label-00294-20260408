<template>
  <div class="page-container">
    <div class="page-header">
      <el-button @click="router.back()" class="back-btn">
        <el-icon><ArrowLeft /></el-icon>
        返回列表
      </el-button>
    </div>
    
    <div class="create-content">
      <div class="card-container form-card">
        <h2 class="form-title">
          <el-icon><Plus /></el-icon>
          新建订单
        </h2>
        
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-position="top"
          class="order-form"
        >
          <!-- 收货信息 -->
          <div class="form-section">
            <h3 class="section-title">
              <el-icon><Location /></el-icon>
              收货信息
            </h3>
            
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="联系电话" prop="contact_phone">
                  <el-input
                    v-model="form.contact_phone"
                    placeholder="请输入联系电话"
                    size="large"
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
                v-model="form.shipping_address"
                type="textarea"
                :rows="3"
                placeholder="请输入详细收货地址"
              />
            </el-form-item>
          </div>
          
          <!-- 商品信息 -->
          <div class="form-section">
            <h3 class="section-title">
              <el-icon><ShoppingCart /></el-icon>
              商品信息
            </h3>
            
            <div class="items-list">
              <transition-group name="item">
                <div
                  v-for="(item, index) in form.items"
                  :key="index"
                  class="item-row"
                >
                  <div class="item-index">{{ index + 1 }}</div>
                  
                  <el-form-item
                    :prop="`items.${index}.product_name`"
                    :rules="{ required: true, message: '请输入商品名称', trigger: 'blur' }"
                    class="item-field name-field"
                  >
                    <el-input
                      v-model="item.product_name"
                      placeholder="商品名称"
                    />
                  </el-form-item>
                  
                  <el-form-item
                    :prop="`items.${index}.price`"
                    :rules="{ required: true, message: '请输入单价', trigger: 'blur' }"
                    class="item-field price-field"
                  >
                    <el-input-number
                      v-model="item.price"
                      :min="0.01"
                      :precision="2"
                      :controls="false"
                      placeholder="单价"
                    />
                  </el-form-item>
                  
                  <el-form-item
                    :prop="`items.${index}.quantity`"
                    :rules="{ required: true, message: '请输入数量', trigger: 'blur' }"
                    class="item-field quantity-field"
                  >
                    <el-input-number
                      v-model="item.quantity"
                      :min="1"
                      :controls="true"
                      placeholder="数量"
                    />
                  </el-form-item>
                  
                  <div class="item-subtotal">
                    ¥{{ (item.price * item.quantity || 0).toFixed(2) }}
                  </div>
                  
                  <el-button
                    type="danger"
                    :icon="Delete"
                    circle
                    @click="removeItem(index)"
                    :disabled="form.items.length <= 1"
                  />
                </div>
              </transition-group>
            </div>
            
            <el-button type="primary" plain @click="addItem" class="add-item-btn">
              <el-icon><Plus /></el-icon>
              添加商品
            </el-button>
          </div>
          
          <!-- 订单汇总 -->
          <div class="order-summary">
            <div class="summary-row">
              <span>商品数量</span>
              <span>{{ totalQuantity }} 件</span>
            </div>
            <div class="summary-row total">
              <span>订单总额</span>
              <span class="total-amount">¥{{ totalAmount.toFixed(2) }}</span>
            </div>
          </div>
          
          <!-- 提交按钮 -->
          <div class="form-actions">
            <el-button size="large" @click="handleCancel">取消</el-button>
            <el-button type="primary" size="large" :loading="loading" @click="handleSubmit">
              <el-icon><Check /></el-icon>
              提交订单
            </el-button>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useOrderStore } from '@/store/orders'
import { toast, notify } from '@/utils/toast'
import { 
  ArrowLeft, Plus, Location, Phone, ShoppingCart, 
  Delete, Check
} from '@element-plus/icons-vue'

const router = useRouter()
const orderStore = useOrderStore()

const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  shipping_address: '',
  contact_phone: '',
  items: [
    { product_name: '', price: 0, quantity: 1 }
  ]
})

const rules = {
  shipping_address: [
    { required: true, message: '请输入收货地址', trigger: 'blur' }
  ],
  contact_phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

const totalQuantity = computed(() => {
  return form.items.reduce((sum, item) => sum + (item.quantity || 0), 0)
})

const totalAmount = computed(() => {
  return form.items.reduce((sum, item) => sum + (item.price || 0) * (item.quantity || 0), 0)
})

const addItem = () => {
  form.items.push({ product_name: '', price: 0, quantity: 1 })
  toast.info('已添加新商品')
}

const removeItem = (index) => {
  if (form.items.length > 1) {
    form.items.splice(index, 1)
    toast.info('已移除商品')
  } else {
    toast.warning('至少保留一个商品')
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      // 验证商品信息
      const hasInvalidItem = form.items.some(
        item => !item.product_name || item.price <= 0 || item.quantity <= 0
      )
      if (hasInvalidItem) {
        toast.warning('请完善商品信息')
        return
      }
      
      loading.value = true
      try {
        const order = await orderStore.createOrder(form)
        notify.success('创建成功', `订单 ${order.order_number} 已创建`)
        router.push('/orders')
      } catch (error) {
        toast.error(error.message || '订单创建失败')
      } finally {
        loading.value = false
      }
    } else {
      toast.warning('请完善表单信息')
    }
  })
}

const handleCancel = () => {
  router.back()
}
</script>

<style scoped lang="scss">
.page-header {
  margin-bottom: 24px;
  
  .back-btn {
    font-weight: 500;
  }
}

.create-content {
  max-width: 900px;
}

.form-card {
  .form-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 22px;
    font-weight: 700;
    color: #1f2937;
    margin: 0 0 32px 0;
    
    .el-icon {
      color: #6366f1;
    }
  }
}

.form-section {
  margin-bottom: 32px;
  padding-bottom: 32px;
  border-bottom: 1px solid #e5e7eb;
  
  &:last-of-type {
    border-bottom: none;
  }
  
  .section-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
    color: #374151;
    margin: 0 0 20px 0;
    
    .el-icon {
      color: #6366f1;
    }
  }
}

.items-list {
  .item-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 16px;
    background: #f9fafb;
    border-radius: 12px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
    
    &:hover {
      background: #f3f4f6;
    }
    
    .item-index {
      width: 28px;
      height: 28px;
      background: #6366f1;
      color: white;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 600;
      flex-shrink: 0;
      margin-top: 4px;
    }
    
    .item-field {
      margin-bottom: 0;
      
      &.name-field {
        flex: 1;
        min-width: 200px;
      }
      
      &.price-field {
        width: 140px;
      }
      
      &.quantity-field {
        width: 120px;
      }
    }
    
    .item-subtotal {
      width: 100px;
      text-align: right;
      font-weight: 600;
      color: #ef4444;
      font-size: 15px;
      padding-top: 8px;
    }
  }
}

.add-item-btn {
  margin-top: 8px;
}

.order-summary {
  background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 32px;
  
  .summary-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    font-size: 14px;
    color: #6b7280;
    
    &.total {
      font-size: 16px;
      font-weight: 600;
      color: #1f2937;
      padding-top: 12px;
      margin-top: 8px;
      border-top: 1px dashed #c4b5fd;
      
      .total-amount {
        font-size: 28px;
        color: #6366f1;
      }
    }
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

// 列表动画
.item-enter-active,
.item-leave-active {
  transition: all 0.3s ease;
}

.item-enter-from,
.item-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
