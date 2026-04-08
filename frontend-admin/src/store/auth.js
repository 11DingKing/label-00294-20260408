import { defineStore } from 'pinia'
import { login, logout, getUserInfo, changePassword } from '@/api/auth'
import { ElMessage } from 'element-plus'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    refreshToken: localStorage.getItem('refreshToken') || '',
    user: JSON.parse(localStorage.getItem('user') || 'null')
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    username: (state) => state.user?.username || ''
  },

  actions: {
    async login(credentials) {
      try {
        const response = await login(credentials)
        if (response.code === 200) {
          this.token = response.data.access_token
          this.refreshToken = response.data.refresh_token
          this.user = response.data.user
          
          localStorage.setItem('token', this.token)
          localStorage.setItem('refreshToken', this.refreshToken)
          localStorage.setItem('user', JSON.stringify(this.user))
          
          return true
        }
        return false
      } catch (error) {
        ElMessage({
          message: error.message || '登录失败，请检查用户名和密码',
          type: 'error',
          duration: 3000,
          showClose: true
        })
        return false
      }
    },

    async logout() {
      try {
        if (this.refreshToken) {
          await logout({ refresh_token: this.refreshToken })
        }
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.token = ''
        this.refreshToken = ''
        this.user = null
        localStorage.removeItem('token')
        localStorage.removeItem('refreshToken')
        localStorage.removeItem('user')
      }
    },

    async fetchUserInfo() {
      try {
        const response = await getUserInfo()
        if (response.code === 200) {
          this.user = response.data
          localStorage.setItem('user', JSON.stringify(this.user))
        }
      } catch (error) {
        console.error('Fetch user info error:', error)
      }
    },

    async changePassword(oldPassword, newPassword) {
      try {
        const response = await changePassword({
          old_password: oldPassword,
          new_password: newPassword
        })
        if (response.code === 200) {
          return true
        }
        return false
      } catch (error) {
        return false
      }
    }
  }
})
