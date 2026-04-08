import api from './index'

export const login = (data) => {
  return api.post('/auth/login/', data)
}

export const logout = (data) => {
  return api.post('/auth/logout/', data)
}

export const getUserInfo = () => {
  return api.get('/auth/user/')
}

export const changePassword = (data) => {
  return api.post('/auth/change-password/', data)
}

export const refreshToken = (refreshToken) => {
  return api.post('/token/refresh/', { refresh: refreshToken })
}
