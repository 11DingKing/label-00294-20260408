import api from './index'

export const getOrders = (params) => {
  return api.get('/orders/', { params })
}

export const getOrderDetail = (id) => {
  return api.get(`/orders/${id}/`)
}

export const createOrder = (data) => {
  return api.post('/orders/', data)
}

export const updateOrder = (id, data) => {
  return api.put(`/orders/${id}/`, data)
}

export const deleteOrder = (id) => {
  return api.delete(`/orders/${id}/`)
}

export const updateOrderStatus = (id, status) => {
  return api.patch(`/orders/${id}/status/`, { status })
}

export const getOrderItems = (orderId) => {
  return api.get(`/orders/${orderId}/items/`)
}

export const addOrderItem = (orderId, data) => {
  return api.post(`/orders/${orderId}/items/`, data)
}

export const deleteOrderItem = (orderId, itemId) => {
  return api.delete(`/orders/${orderId}/items/${itemId}/`)
}

export const getStatistics = (params) => {
  return api.get('/orders/statistics/', { params })
}
