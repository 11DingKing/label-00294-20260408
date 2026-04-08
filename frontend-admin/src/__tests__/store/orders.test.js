/**
 * Orders Store 测试用例
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useOrderStore } from '@/store/orders'
import * as ordersApi from '@/api/orders'

// Mock API
vi.mock('@/api/orders', () => ({
  getOrders: vi.fn(),
  getOrderDetail: vi.fn(),
  createOrder: vi.fn(),
  updateOrder: vi.fn(),
  deleteOrder: vi.fn(),
  updateOrderStatus: vi.fn()
}))

describe('Orders Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  describe('initial state', () => {
    it('should have correct initial state', () => {
      const store = useOrderStore()
      expect(store.orders).toEqual([])
      expect(store.currentOrder).toBeNull()
      expect(store.total).toBe(0)
      expect(store.loading).toBe(false)
    })
  })

  describe('fetchOrders action', () => {
    it('should fetch orders with pagination', async () => {
      const store = useOrderStore()
      const mockOrders = [
        { id: 1, order_number: 'ORD001' },
        { id: 2, order_number: 'ORD002' }
      ]
      ordersApi.getOrders.mockResolvedValue({
        code: 200,
        data: { results: mockOrders, count: 2 }
      })

      await store.fetchOrders({ page: 1, page_size: 10 })

      expect(store.orders).toEqual(mockOrders)
      expect(store.total).toBe(2)
      expect(store.loading).toBe(false)
    })

    it('should handle non-paginated response', async () => {
      const store = useOrderStore()
      const mockOrders = [{ id: 1, order_number: 'ORD001' }]
      ordersApi.getOrders.mockResolvedValue({
        code: 200,
        data: mockOrders
      })

      await store.fetchOrders()

      expect(store.orders).toEqual(mockOrders)
      expect(store.total).toBe(1)
    })

    it('should set loading state during fetch', async () => {
      const store = useOrderStore()
      ordersApi.getOrders.mockImplementation(() => {
        expect(store.loading).toBe(true)
        return Promise.resolve({ code: 200, data: { results: [], count: 0 } })
      })

      await store.fetchOrders()

      expect(store.loading).toBe(false)
    })
  })

  describe('fetchOrderDetail action', () => {
    it('should fetch order detail', async () => {
      const store = useOrderStore()
      const mockOrder = {
        id: 1,
        order_number: 'ORD001',
        items: [{ id: 1, product_name: '商品1' }]
      }
      ordersApi.getOrderDetail.mockResolvedValue({
        code: 200,
        data: mockOrder
      })

      await store.fetchOrderDetail(1)

      expect(store.currentOrder).toEqual(mockOrder)
    })

    it('should throw error on fetch failure', async () => {
      const store = useOrderStore()
      ordersApi.getOrderDetail.mockRejectedValue(new Error('Not found'))

      await expect(store.fetchOrderDetail(999)).rejects.toThrow()
    })
  })

  describe('createOrder action', () => {
    it('should create order and return data', async () => {
      const store = useOrderStore()
      const orderData = {
        shipping_address: '北京市',
        contact_phone: '13800138000',
        items: [{ product_name: '商品', price: 99, quantity: 1 }]
      }
      const mockResponse = { id: 1, order_number: 'ORD001' }
      ordersApi.createOrder.mockResolvedValue({
        code: 201,
        data: mockResponse
      })

      const result = await store.createOrder(orderData)

      expect(result).toEqual(mockResponse)
    })

    it('should throw error on create failure', async () => {
      const store = useOrderStore()
      ordersApi.createOrder.mockResolvedValue({
        code: 400,
        message: '创建失败'
      })

      await expect(store.createOrder({})).rejects.toThrow('创建失败')
    })
  })

  describe('updateOrder action', () => {
    it('should update order and return data', async () => {
      const store = useOrderStore()
      const updateData = { shipping_address: '新地址' }
      const mockResponse = { id: 1, shipping_address: '新地址' }
      ordersApi.updateOrder.mockResolvedValue({
        code: 200,
        data: mockResponse
      })

      const result = await store.updateOrder(1, updateData)

      expect(result).toEqual(mockResponse)
    })
  })

  describe('removeOrder action', () => {
    it('should delete order and return true', async () => {
      const store = useOrderStore()
      ordersApi.deleteOrder.mockResolvedValue({ code: 200 })

      const result = await store.removeOrder(1)

      expect(result).toBe(true)
    })

    it('should throw error on delete failure', async () => {
      const store = useOrderStore()
      ordersApi.deleteOrder.mockResolvedValue({
        code: 400,
        message: '删除失败'
      })

      await expect(store.removeOrder(1)).rejects.toThrow('删除失败')
    })
  })

  describe('changeOrderStatus action', () => {
    it('should update order status', async () => {
      const store = useOrderStore()
      const mockResponse = { id: 1, status: 'processing' }
      ordersApi.updateOrderStatus.mockResolvedValue({
        code: 200,
        data: mockResponse
      })

      const result = await store.changeOrderStatus(1, 'processing')

      expect(result).toEqual(mockResponse)
    })
  })
})
