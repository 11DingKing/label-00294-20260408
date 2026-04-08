# 订单管理系统 - 前端

基于 Vue 3 + Element Plus 的订单管理前端应用。

## 技术栈

- Vue 3
- Vite
- Element Plus
- Pinia (状态管理)
- Vue Router
- Axios
- SCSS

## 目录结构

```
frontend-admin/
├── src/
│   ├── api/                # API 接口封装
│   │   ├── index.js        # Axios 实例配置
│   │   ├── auth.js         # 认证接口
│   │   └── orders.js       # 订单接口
│   ├── store/              # Pinia 状态管理
│   │   ├── auth.js         # 认证状态
│   │   └── orders.js       # 订单状态
│   ├── views/              # 页面视图
│   │   ├── Login.vue       # 登录页
│   │   ├── Orders.vue      # 订单列表
│   │   └── OrderDetail.vue # 订单详情
│   ├── layouts/            # 布局组件
│   │   └── MainLayout.vue  # 主布局
│   ├── router/             # 路由配置
│   ├── styles/             # 全局样式
│   ├── utils/              # 工具函数
│   ├── App.vue             # 根组件
│   └── main.js             # 入口文件
├── public/                 # 静态资源
├── index.html              # HTML 模板
├── vite.config.js          # Vite 配置
├── vitest.config.js        # 测试配置
├── package.json            # 项目依赖
└── Dockerfile              # Docker 构建文件
```

## 本地开发

### 环境要求

- Node.js 18+
- npm 或 yarn

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

开发服务器默认运行在 http://localhost:5173

### 构建生产版本

```bash
npm run build
```

构建产物输出到 `dist/` 目录。

## Docker 部署

```bash
docker build -t order-frontend .
docker run -p 8091:8091 order-frontend
```

## 功能特性

- 用户登录/退出
- 订单列表（分页、搜索、筛选）
- 订单创建（弹窗表单）
- 订单详情查看/编辑
- 订单状态管理
- 订单导出 (CSV)
- 修改密码
- Toast 消息提示

## 运行测试

```bash
# 运行所有测试
npm run test

# 单次运行（非 watch 模式）
npx vitest --run
```

## 环境变量

在 `vite.config.js` 中配置 API 代理：

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8010',
      changeOrigin: true
    }
  }
}
```

## 访问地址

- 开发环境：http://localhost:5173
- 生产环境：http://localhost:8091

## 默认账号

- 用户名：admin
- 密码：admin123
