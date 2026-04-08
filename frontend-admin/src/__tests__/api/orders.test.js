/**
 * 订单API测试用例
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import api from '@/api/index'
import {
  getOrders,
  getOrderDetail,
  createOrder,
  updateOrder,
  deleteOrder,
  updateOrderStatus,
  getOrderItems,
  addOrderItem,
  deleteOrderItem
} from '@/api/orders'

// Mock api
vi.mock('@/api/index', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn()
  }
}))

describe('Orders API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getOrders', () => {
    it('should call api.get with correct parameters', async () => {
      const params = { page: 1, page_size: 10 }
      const mockResponse = {
        code: 200,
        data: { results: [], count: 0 }
      }
      api.get.mockResolvedValue(mockResponse)

      const result = await getOrders(params)

      expect(api.get).toHaveBeenCalledWith('/orders/', { params })
      expect(result).toEqual(mockResponse)
    })

    it('should handle filter parameters', async () => {
      const params = { page: 1, status: 'pending', order_number: 'ORD001' }
      api.get.mockResolvedValue({ code: 200, data: { results: [] } })

      await getOrders(params)

      expect(api.get).toHaveBeenCalledWith('/orders/', { params })
    })
  })

  describe('getOrderDetail', () => {
    it('should call api.get with order id', async () => {
      const orderId = 1
      const mockResponse = {
        code: 200,
        data: { id: 1, order_number: 'ORD001' }
      }
      api.get.mockResolvedValue(mockResponse)

      const result = await getOrderDetail(orderId)

      expect(api.get).toHaveBeenCalledWith('/orders/1/')
      expect(result).toEqual(mockResponse)
    })
  })

  describe('createOrder', () => {
    it('should call api.post with order data', async () => {
      const orderData = {
        shipping_address: '北京市',
        contact_phone: '13800138000',
        items: [{ product_name: '商品1', price: 99, quantity: 1 }]
      }
      const mockResponse = {
        code: 201,
        data: { id: 1, order_number: 'ORD001' }
      }
      api.post.mockResolvedValue(mockResponse)

      const result = await createOrder(orderData)

      expect(api.post).toHaveBeenCalledWith('/orders/', orderData)
      expect(result).toEqual(mockResponse)
    })
  })

  describe('updateOrder', () => {
    it('should call api.put with order id and data', async () => {
      const orderId = 1
      const updateData = {
        shipping_address: '新地址',
        contact_phone: '13900139000'
      }
      const mockResponse = { code: 200, data: { id: 1 } }
      api.put.mockResolvedValue(mockResponse)

      const result = await updateOrder(orderId, updateData)

      expect(api.put).toHaveBeenCalledWith('/orders/1/', updateData)
      expect(result).toEqual(mockResponse)
    })
  })

  describe('deleteOrder', () => {
    it('should call api.delete with order id', async () => {
      const orderId = 1
      const mockResponse = { code: 200, message: '删除成功' }
      api.delete.mockResolvedValue(mockResponse)

      const result = await deleteOrder(orderId)

      expect(api.delete).toHaveBeenCalledWith('/orders/1/')
      expect(result).toEqual(mockResponse)
    })
  })

  describe('updateOrderStatus', () => {
    it('should call api.patch with order id and status', async () => {
      const orderId = 1
      const status = 'processing'
      const mockResponse = { code: 200, data: { status: 'processing' } }
      api.patch.mockResolvedValue(mockResponse)

      const result = await updateOrderStatus(orderId, status)

      expect(api.patch).toHaveBeenCalledWith('/orders/1/status/', { status })
      expect(result).toEqual(mockResponse)
    })
  })

  describe('getOrderItems', () => {
    it('should call api.get with order id', async () => {
      const orderId = 1
      const mockResponse = {
        code: 200,
        data: [{ id: 1, product_name: '商品1' }]
      }
      api.get.mockResolvedValue(mockResponse)

      const result = await getOrderItems(orderId)

      expect(api.get).toHaveBeenCalledWith('/orders/1/items/')
      expect(result).toEqual(mockResponse)
    })
  })

  describe('addOrderItem', () => {
    it('should call api.post with order id and item data', async () => {
      const orderId = 1
      const itemData = { product_name: '新商品', price: 50, quantity: 2 }
      const mockResponse = { code: 201, data: { id: 2 } }
      api.post.mockResolvedValue(mockResponse)

      const result = await addOrderItem(orderId, itemData)

      expect(api.post).toHaveBeenCalledWith('/orders/1/items/', itemData)
      expect(result).toEqual(mockResponse)
    })
  })

  describe('deleteOrderItem', () => {
    it('should call api.delete with order id and item id', async () => {
      const orderId = 1
      const itemId = 2
      const mockResponse = { code: 200, message: '删除成功' }
      api.delete.mockResolvedValue(mockResponse)

      const result = await deleteOrderItem(orderId, itemId)

      expect(api.delete).toHaveBeenCalledWith('/orders/1/items/2/')
      expect(result).toEqual(mockResponse)
    })
  })
})
