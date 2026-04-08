/**
 * 认证API测试用例
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import api from '@/api/index'
import { login, logout, getUserInfo, changePassword, refreshToken } from '@/api/auth'

// Mock api
vi.mock('@/api/index', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn()
  }
}))

describe('Auth API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('login', () => {
    it('should call api.post with correct parameters', async () => {
      const credentials = { username: 'testuser', password: 'testpass123' }
      const mockResponse = {
        code: 200,
        data: {
          access_token: 'mock_access_token',
          refresh_token: 'mock_refresh_token',
          user: { id: 1, username: 'testuser' }
        }
      }
      api.post.mockResolvedValue(mockResponse)

      const result = await login(credentials)

      expect(api.post).toHaveBeenCalledWith('/auth/login/', credentials)
      expect(result).toEqual(mockResponse)
    })

    it('should handle login error', async () => {
      const credentials = { username: 'testuser', password: 'wrongpass' }
      api.post.mockRejectedValue(new Error('用户名或密码错误'))

      await expect(login(credentials)).rejects.toThrow('用户名或密码错误')
    })
  })

  describe('logout', () => {
    it('should call api.post with refresh token', async () => {
      const data = { refresh_token: 'mock_refresh_token' }
      const mockResponse = { code: 200, message: '退出成功' }
      api.post.mockResolvedValue(mockResponse)

      const result = await logout(data)

      expect(api.post).toHaveBeenCalledWith('/auth/logout/', data)
      expect(result).toEqual(mockResponse)
    })
  })

  describe('getUserInfo', () => {
    it('should call api.get and return user info', async () => {
      const mockResponse = {
        code: 200,
        data: { id: 1, username: 'testuser', email: 'test@example.com' }
      }
      api.get.mockResolvedValue(mockResponse)

      const result = await getUserInfo()

      expect(api.get).toHaveBeenCalledWith('/auth/user/')
      expect(result).toEqual(mockResponse)
    })
  })

  describe('changePassword', () => {
    it('should call api.post with password data', async () => {
      const data = { old_password: 'oldpass', new_password: 'newpass' }
      const mockResponse = { code: 200, message: '密码修改成功' }
      api.post.mockResolvedValue(mockResponse)

      const result = await changePassword(data)

      expect(api.post).toHaveBeenCalledWith('/auth/change-password/', data)
      expect(result).toEqual(mockResponse)
    })
  })

  describe('refreshToken', () => {
    it('should call api.post with refresh token', async () => {
      const token = 'mock_refresh_token'
      const mockResponse = { access: 'new_access_token' }
      api.post.mockResolvedValue(mockResponse)

      const result = await refreshToken(token)

      expect(api.post).toHaveBeenCalledWith('/token/refresh/', { refresh: token })
      expect(result).toEqual(mockResponse)
    })
  })
})
