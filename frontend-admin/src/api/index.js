import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// Token 刷新状态
let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

// 获取 store（延迟导入避免循环依赖）
const getAuthStore = () => {
  const { useAuthStore } = require('@/store/auth')
  return useAuthStore()
}

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code === 200 || res.code === 201) {
      return res
    } else {
      ElMessage({
        message: res.message || '请求失败',
        type: 'error',
        duration: 3000,
        showClose: true
      })
      return Promise.reject(new Error(res.message || '请求失败'))
    }
  },
  async error => {
    const originalRequest = error.config
    
    if (error.response) {
      const { status, data } = error.response
      
      // Token 过期，尝试刷新
      if (status === 401 && !originalRequest._retry) {
        const refreshToken = localStorage.getItem('refreshToken')
        
        // 没有 refresh token 或者是刷新请求本身失败
        if (!refreshToken || originalRequest.url === '/token/refresh/') {
          const authStore = getAuthStore()
          authStore.logout()
          router.push('/login')
          return Promise.reject(error)
        }
        
        if (isRefreshing) {
          // 正在刷新，将请求加入队列
          return new Promise((resolve, reject) => {
            failedQueue.push({ resolve, reject })
          }).then(token => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            return api(originalRequest)
          }).catch(err => {
            return Promise.reject(err)
          })
        }
        
        originalRequest._retry = true
        isRefreshing = true
        
        try {
          const response = await axios.post('/api/token/refresh/', {
            refresh: refreshToken
          })
          
          const newToken = response.data.access
          localStorage.setItem('token', newToken)
          
          // 如果返回了新的 refresh token
          if (response.data.refresh) {
            localStorage.setItem('refreshToken', response.data.refresh)
          }
          
          api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
          originalRequest.headers.Authorization = `Bearer ${newToken}`
          
          processQueue(null, newToken)
          
          return api(originalRequest)
        } catch (refreshError) {
          processQueue(refreshError, null)
          const authStore = getAuthStore()
          authStore.logout()
          router.push('/login')
          return Promise.reject(refreshError)
        } finally {
          isRefreshing = false
        }
      }
      
      ElMessage({
        message: data?.message || `请求失败: ${status}`,
        type: 'error',
        duration: 3000,
        showClose: true
      })
    } else {
      ElMessage({
        message: '网络错误，请检查网络连接',
        type: 'error',
        duration: 3000,
        showClose: true
      })
    }
    return Promise.reject(error)
  }
)

export default api
