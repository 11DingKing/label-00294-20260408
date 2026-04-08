import { defineStore } from 'pinia'
import {
  getOrders,
  getOrderDetail,
  createOrder,
  updateOrder,
  deleteOrder,
  updateOrderStatus
} from '@/api/orders'

export const useOrderStore = defineStore('orders', {
  state: () => ({
    orders: [],
    currentOrder: null,
    total: 0,
    loading: false
  }),

  actions: {
    async fetchOrders(params = {}) {
      this.loading = true
      try {
        const response = await getOrders(params)
        if (response.code === 200) {
          if (response.data.results) {
            // 分页响应
            this.orders = response.data.results
            this.total = response.data.count
          } else {
            // 非分页响应
            this.orders = Array.isArray(response.data) ? response.data : []
            this.total = this.orders.length
          }
        }
      } catch (error) {
        console.error('Fetch orders error:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchOrderDetail(id) {
      try {
        const response = await getOrderDetail(id)
        if (response.code === 200) {
          this.currentOrder = response.data
        }
      } catch (error) {
        console.error('Fetch order detail error:', error)
        throw error
      }
    },

    async createOrder(data) {
      try {
        const response = await createOrder(data)
        if (response.code === 201) {
          return response.data
        }
        throw new Error(response.message)
      } catch (error) {
        console.error('Create order error:', error)
        throw error
      }
    },

    async updateOrder(id, data) {
      try {
        const response = await updateOrder(id, data)
        if (response.code === 200) {
          return response.data
        }
        throw new Error(response.message)
      } catch (error) {
        console.error('Update order error:', error)
        throw error
      }
    },

    async removeOrder(id) {
      try {
        const response = await deleteOrder(id)
        if (response.code === 200) {
          return true
        }
        throw new Error(response.message)
      } catch (error) {
        console.error('Delete order error:', error)
        throw error
      }
    },

    async changeOrderStatus(id, status) {
      try {
        const response = await updateOrderStatus(id, status)
        if (response.code === 200) {
          return response.data
        }
        throw new Error(response.message)
      } catch (error) {
        console.error('Update order status error:', error)
        throw error
      }
    }
  }
})
