/**
 * Auth Store 测试用例
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/store/auth'
import * as authApi from '@/api/auth'

// Mock API
vi.mock('@/api/auth', () => ({
  login: vi.fn(),
  logout: vi.fn(),
  getUserInfo: vi.fn(),
  changePassword: vi.fn()
}))

// Mock Element Plus
vi.mock('element-plus', () => ({
  ElMessage: {
    success: vi.fn(),
    error: vi.fn(),
    warning: vi.fn(),
    info: vi.fn()
  }
}))

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.clearAllMocks()
  })

  afterEach(() => {
    localStorage.clear()
  })

  describe('initial state', () => {
    it('should have empty initial state', () => {
      const store = useAuthStore()
      expect(store.token).toBe('')
      expect(store.refreshToken).toBe('')
      expect(store.user).toBeNull()
    })

    it('should load state from localStorage', () => {
      localStorage.setItem('token', 'stored_token')
      localStorage.setItem('refreshToken', 'stored_refresh')
      localStorage.setItem('user', JSON.stringify({ id: 1, username: 'test' }))

      const store = useAuthStore()
      expect(store.token).toBe('stored_token')
      expect(store.refreshToken).toBe('stored_refresh')
      expect(store.user).toEqual({ id: 1, username: 'test' })
    })
  })

  describe('getters', () => {
    it('isAuthenticated should return true when token exists', () => {
      const store = useAuthStore()
      store.token = 'some_token'
      expect(store.isAuthenticated).toBe(true)
    })

    it('isAuthenticated should return false when token is empty', () => {
      const store = useAuthStore()
      expect(store.isAuthenticated).toBe(false)
    })

    it('username should return user username', () => {
      const store = useAuthStore()
      store.user = { username: 'testuser' }
      expect(store.username).toBe('testuser')
    })

    it('username should return empty string when no user', () => {
      const store = useAuthStore()
      expect(store.username).toBe('')
    })
  })

  describe('login action', () => {
    it('should login successfully and store tokens', async () => {
      const store = useAuthStore()
      const mockResponse = {
        code: 200,
        data: {
          access_token: 'access_token',
          refresh_token: 'refresh_token',
          user: { id: 1, username: 'testuser' }
        }
      }
      authApi.login.mockResolvedValue(mockResponse)

      const result = await store.login({ username: 'testuser', password: 'pass' })

      expect(result).toBe(true)
      expect(store.token).toBe('access_token')
      expect(store.refreshToken).toBe('refresh_token')
      expect(store.user).toEqual({ id: 1, username: 'testuser' })
      expect(localStorage.getItem('token')).toBe('access_token')
    })

    it('should return false on login failure', async () => {
      const store = useAuthStore()
      authApi.login.mockRejectedValue(new Error('Login failed'))

      const result = await store.login({ username: 'test', password: 'wrong' })

      expect(result).toBe(false)
      expect(store.token).toBe('')
    })
  })

  describe('logout action', () => {
    it('should clear all auth data on logout', async () => {
      const store = useAuthStore()
      store.token = 'token'
      store.refreshToken = 'refresh'
      store.user = { id: 1 }
      localStorage.setItem('token', 'token')
      localStorage.setItem('refreshToken', 'refresh')
      localStorage.setItem('user', JSON.stringify({ id: 1 }))

      authApi.logout.mockResolvedValue({ code: 200 })

      await store.logout()

      expect(store.token).toBe('')
      expect(store.refreshToken).toBe('')
      expect(store.user).toBeNull()
      expect(localStorage.getItem('token')).toBeNull()
    })

    it('should clear data even if logout API fails', async () => {
      const store = useAuthStore()
      store.token = 'token'
      store.refreshToken = 'refresh'
      authApi.logout.mockRejectedValue(new Error('API error'))

      await store.logout()

      expect(store.token).toBe('')
      expect(store.refreshToken).toBe('')
    })
  })

  describe('fetchUserInfo action', () => {
    it('should fetch and store user info', async () => {
      const store = useAuthStore()
      const mockUser = { id: 1, username: 'testuser', email: 'test@example.com' }
      authApi.getUserInfo.mockResolvedValue({ code: 200, data: mockUser })

      await store.fetchUserInfo()

      expect(store.user).toEqual(mockUser)
      expect(localStorage.getItem('user')).toBe(JSON.stringify(mockUser))
    })
  })

  describe('changePassword action', () => {
    it('should return true on successful password change', async () => {
      const store = useAuthStore()
      authApi.changePassword.mockResolvedValue({ code: 200 })

      const result = await store.changePassword('oldpass', 'newpass')

      expect(result).toBe(true)
      expect(authApi.changePassword).toHaveBeenCalledWith({
        old_password: 'oldpass',
        new_password: 'newpass'
      })
    })

    it('should return false on password change failure', async () => {
      const store = useAuthStore()
      authApi.changePassword.mockRejectedValue(new Error('Failed'))

      const result = await store.changePassword('oldpass', 'newpass')

      expect(result).toBe(false)
    })
  })
})
