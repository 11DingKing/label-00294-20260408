<template>
  <div class="login-container">
    <div class="login-background">
      <div class="gradient-sphere sphere-1"></div>
      <div class="gradient-sphere sphere-2"></div>
      <div class="gradient-sphere sphere-3"></div>
      <div class="grid-pattern"></div>
    </div>
    
    <div class="login-card">
      <div class="login-header">
        <div class="logo-wrapper">
          <div class="logo-icon">
            <el-icon :size="32"><ShoppingBag /></el-icon>
          </div>
        </div>
        <h1 class="login-title">订单管理系统</h1>
        <p class="login-subtitle">欢迎回来，请登录您的账户</p>
      </div>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
            clearable
          >
            <template #prefix>
              <el-icon class="input-icon"><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            show-password
            clearable
            @keyup.enter="handleLogin"
          >
            <template #prefix>
              <el-icon class="input-icon"><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleLogin"
            class="login-button"
          >
            <span v-if="!loading">登 录</span>
            <span v-else>登录中...</span>
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-footer">
        <p>© 2026 订单管理系统 · 安全登录</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { ShoppingBag, User, Lock } from '@element-plus/icons-vue'
import { toast, notify } from '@/utils/toast'

const router = useRouter()
const authStore = useAuthStore()

const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const success = await authStore.login(loginForm)
        if (success) {
          notify.success('登录成功', `欢迎回来，${authStore.username}！`)
          router.push('/')
        }
      } finally {
        loading.value = false
      }
    } else {
      toast.warning('请完善登录信息')
    }
  })
}
</script>

<style scoped lang="scss">
.login-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  overflow: hidden;
  background: #0f172a;
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  
  .gradient-sphere {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.6;
    animation: float 20s infinite ease-in-out;
  }
  
  .sphere-1 {
    width: 600px;
    height: 600px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    top: -200px;
    left: -200px;
    animation-delay: 0s;
  }
  
  .sphere-2 {
    width: 400px;
    height: 400px;
    background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%);
    bottom: -100px;
    right: -100px;
    animation-delay: 7s;
  }
  
  .sphere-3 {
    width: 300px;
    height: 300px;
    background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
    top: 50%;
    right: 20%;
    animation-delay: 14s;
  }
  
  .grid-pattern {
    position: absolute;
    width: 100%;
    height: 100%;
    background-image: 
      linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
    background-size: 60px 60px;
  }
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.05);
  }
  66% {
    transform: translate(-20px, 30px) scale(0.95);
  }
}

.login-card {
  position: relative;
  z-index: 1;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  padding: 48px 44px;
  width: 440px;
  animation: cardEnter 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes cardEnter {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 36px;
  
  .logo-wrapper {
    display: inline-flex;
    margin-bottom: 20px;
    
    .logo-icon {
      width: 64px;
      height: 64px;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.5);
    }
  }
  
  .login-title {
    color: #1f2937;
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
  }
  
  .login-subtitle {
    color: #6b7280;
    font-size: 15px;
    margin: 0;
  }
}

.login-form {
  .input-icon {
    color: #9ca3af;
  }
  
  :deep(.el-input__wrapper) {
    padding: 4px 16px;
    height: 50px;
    background: #f9fafb;
    border: 2px solid transparent;
    box-shadow: none !important;
    
    &:hover {
      border-color: #e5e7eb;
    }
    
    &.is-focus {
      background: white;
      border-color: #6366f1;
    }
  }
  
  :deep(.el-form-item) {
    margin-bottom: 20px;
  }
  
  .login-button {
    width: 100%;
    height: 50px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 12px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border: none;
    margin-top: 8px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    
    &:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 12px 24px -8px rgba(99, 102, 241, 0.5);
    }
    
    &:active {
      transform: translateY(0);
    }
  }
}

.login-footer {
  text-align: center;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
  
  p {
    color: #9ca3af;
    font-size: 13px;
    margin: 0;
  }
}
</style>
