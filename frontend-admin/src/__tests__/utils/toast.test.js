/**
 * Toast 工具测试用例
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ElMessage, ElNotification } from 'element-plus'
import { toast, notify } from '@/utils/toast'

// Mock Element Plus
vi.mock('element-plus', () => ({
  ElMessage: vi.fn(),
  ElNotification: vi.fn()
}))

describe('Toast Utils', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('toast', () => {
    it('should call ElMessage with success type', () => {
      toast.success('操作成功')

      expect(ElMessage).toHaveBeenCalledWith(
        expect.objectContaining({
          message: '操作成功',
          type: 'success',
          showClose: true,
          grouping: true
        })
      )
    })

    it('should call ElMessage with error type', () => {
      toast.error('操作失败')

      expect(ElMessage).toHaveBeenCalledWith(
        expect.objectContaining({
          message: '操作失败',
          type: 'error',
          duration: 4000
        })
      )
    })

    it('should call ElMessage with warning type', () => {
      toast.warning('警告信息')

      expect(ElMessage).toHaveBeenCalledWith(
        expect.objectContaining({
          message: '警告信息',
          type: 'warning'
        })
      )
    })

    it('should call ElMessage with info type', () => {
      toast.info('提示信息')

      expect(ElMessage).toHaveBeenCalledWith(
        expect.objectContaining({
          message: '提示信息',
          type: 'info'
        })
      )
    })

    it('should allow custom options', () => {
      toast.success('自定义', { duration: 5000 })

      expect(ElMessage).toHaveBeenCalledWith(
        expect.objectContaining({
          message: '自定义',
          duration: 5000
        })
      )
    })
  })

  describe('notify', () => {
    it('should call ElNotification with success type', () => {
      notify.success('标题', '内容')

      expect(ElNotification).toHaveBeenCalledWith(
        expect.objectContaining({
          title: '标题',
          message: '内容',
          type: 'success',
          position: 'top-right'
        })
      )
    })

    it('should call ElNotification with error type', () => {
      notify.error('错误', '错误详情')

      expect(ElNotification).toHaveBeenCalledWith(
        expect.objectContaining({
          title: '错误',
          message: '错误详情',
          type: 'error',
          duration: 5000
        })
      )
    })

    it('should call ElNotification with warning type', () => {
      notify.warning('警告', '警告内容')

      expect(ElNotification).toHaveBeenCalledWith(
        expect.objectContaining({
          title: '警告',
          message: '警告内容',
          type: 'warning'
        })
      )
    })

    it('should call ElNotification with info type', () => {
      notify.info('信息', '信息内容')

      expect(ElNotification).toHaveBeenCalledWith(
        expect.objectContaining({
          title: '信息',
          message: '信息内容',
          type: 'info'
        })
      )
    })

    it('should allow custom options', () => {
      notify.success('标题', '内容', { position: 'bottom-right' })

      expect(ElNotification).toHaveBeenCalledWith(
        expect.objectContaining({
          position: 'bottom-right'
        })
      )
    })
  })
})
