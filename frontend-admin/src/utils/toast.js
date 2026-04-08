import { ElMessage, ElNotification } from 'element-plus'

// Toast 提示工具
export const toast = {
  success(message, options = {}) {
    ElMessage({
      message,
      type: 'success',
      duration: 2500,
      showClose: true,
      grouping: true,
      ...options
    })
  },

  error(message, options = {}) {
    ElMessage({
      message,
      type: 'error',
      duration: 4000,
      showClose: true,
      grouping: true,
      ...options
    })
  },

  warning(message, options = {}) {
    ElMessage({
      message,
      type: 'warning',
      duration: 3000,
      showClose: true,
      grouping: true,
      ...options
    })
  },

  info(message, options = {}) {
    ElMessage({
      message,
      type: 'info',
      duration: 2500,
      showClose: true,
      grouping: true,
      ...options
    })
  }
}

// 通知工具
export const notify = {
  success(title, message, options = {}) {
    ElNotification({
      title,
      message,
      type: 'success',
      duration: 3000,
      position: 'top-right',
      ...options
    })
  },

  error(title, message, options = {}) {
    ElNotification({
      title,
      message,
      type: 'error',
      duration: 5000,
      position: 'top-right',
      ...options
    })
  },

  warning(title, message, options = {}) {
    ElNotification({
      title,
      message,
      type: 'warning',
      duration: 4000,
      position: 'top-right',
      ...options
    })
  },

  info(title, message, options = {}) {
    ElNotification({
      title,
      message,
      type: 'info',
      duration: 3000,
      position: 'top-right',
      ...options
    })
  }
}

export default toast
