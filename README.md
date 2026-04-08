# Django订单管理系统

## How to Run

### 前置要求
- Docker 和 Docker Compose
- Git

### 启动步骤

1. **克隆项目（如果从Git仓库）**
   ```bash
   git clone <repository-url>
   cd 294
   ```

2. **启动所有服务**
   ```bash
   docker-compose up --build -d
   ```

3. **初始化数据库（首次运行自动完成）**
   
   系统启动时会自动执行：
   - 数据库迁移
   - 创建管理员账号（admin / admin123）

4. **访问应用**
   - 前端管理后台: http://localhost:8091
   - 后端API: http://localhost:8010
   - Django Admin: http://localhost:8010/admin

### 停止服务
```bash
docker-compose down
```

### 查看日志
```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend-admin
docker-compose logs -f db
```

## Services

### 后端服务 (backend)
- **端口**: 8010 (宿主机) -> 8000 (容器)
- **技术栈**: Django 4.2 + Django REST Framework + MySQL
- **主要功能**:
  - 用户认证（JWT）
  - 订单管理（CRUD）
  - 订单项管理
  - 全局异常处理
  - 日志记录

### 前端服务 (frontend-admin)
- **端口**: 8091
- **技术栈**: Vue 3 + Vite + Element Plus + Pinia
- **主要功能**:
  - 用户登录/退出
  - 订单列表（分页、搜索、筛选）
  - 订单创建
  - 订单详情查看/编辑
  - 订单状态管理

### 数据库服务 (db)
- **端口**: 3307 (宿主机) -> 3306 (容器)
- **技术栈**: MySQL 8.0
- **数据库名**: order_management

## 测试账号

系统启动时会自动创建管理员账号：

- **用户名**: admin
- **密码**: admin123

## 题目内容

### 用户需求
开发一个Django订单管理系统，包含：
- 登录和退出界面
- 规范的目录结构
- 后端使用MySQL数据库
- 完整的订单管理功能

### 实现功能

#### 后端功能
1. **认证模块** (`apps/authentication`)
   - 用户登录（JWT Token认证）
   - 用户退出（Token黑名单）
   - 获取当前用户信息

2. **订单模块** (`apps/orders`)
   - 订单CRUD操作
   - 订单状态管理
   - 订单项管理
   - 订单查询（分页、筛选）

3. **用户模块** (`apps/users`)
   - 用户列表查询（管理员）

#### 前端功能
1. **登录页面**
   - 用户名/密码登录
   - 表单验证
   - 登录状态保持

2. **订单管理页面**
   - 订单列表展示（表格）
   - 订单搜索（订单号、状态）
   - 订单分页
   - 订单创建
   - 订单详情查看/编辑
   - 订单删除
   - 订单状态更新

3. **布局组件**
   - 主布局（Header + Sidebar + Main）
   - 响应式设计

### 技术架构

#### 后端架构
```
backend/
├── config/              # 项目配置
│   ├── settings.py      # Django设置
│   └── urls.py         # 路由配置
├── apps/               # 应用模块
│   ├── authentication/ # 认证模块
│   ├── orders/         # 订单模块
│   └── users/          # 用户模块
└── utils/              # 工具类
    └── exceptions.py   # 全局异常处理
```

#### 前端架构
```
frontend-admin/
├── src/
│   ├── api/            # API接口
│   ├── store/          # Pinia状态管理
│   ├── views/          # 页面视图
│   ├── components/     # 组件
│   ├── router/         # 路由配置
│   └── styles/         # 样式文件
```

### 访问地址

- **前端管理后台**: http://localhost:8091
- **后端API**: http://localhost:8010/api/
- **Django Admin**: http://localhost:8010/admin

### API接口

#### 认证接口
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/logout/` - 用户退出
- `GET /api/auth/user/` - 获取当前用户信息

#### 订单接口
- `GET /api/orders/` - 获取订单列表
- `GET /api/orders/{id}/` - 获取订单详情
- `POST /api/orders/` - 创建订单
- `PUT /api/orders/{id}/` - 更新订单
- `PATCH /api/orders/{id}/status/` - 更新订单状态
- `DELETE /api/orders/{id}/` - 删除订单
- `GET /api/orders/{order_id}/items/` - 获取订单项列表
- `POST /api/orders/{order_id}/items/` - 添加订单项
- `DELETE /api/orders/{order_id}/items/{id}/` - 删除订单项

### 开发说明

#### 后端开发
```bash
# 进入后端容器
docker exec -it order_management_backend bash

# 创建新的Django应用
python manage.py startapp apps/new_app

# 创建数据库迁移
python manage.py makemigrations

# 执行数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

#### 前端开发
```bash
# 进入前端容器
docker exec -it order_management_frontend sh

# 安装新依赖
npm install package-name

# 开发模式（如果需要）
npm run dev
```

### 项目特点

1. **模块化设计**: 清晰的分层架构，便于维护和扩展
2. **全局异常处理**: 统一的错误响应格式
3. **日志记录**: 关键操作都有日志记录
4. **数据验证**: 前后端双重验证
5. **美观的UI**: 使用Element Plus组件库，统一的视觉风格
6. **Docker化部署**: 一键启动，环境隔离

### 测试

#### 运行后端测试用例

```bash
# 进入后端容器
docker exec -it order_management_backend bash

# 运行所有测试
python manage.py test apps.authentication apps.orders apps.users --verbosity=2

# 或运行特定模块的测试
python manage.py test apps.orders --verbosity=2
```

#### 测试覆盖范围

- **认证模块测试** (`apps/authentication/tests.py`)
  - 登录成功/失败场景
  - 退出登录
  - 获取用户信息
  - 未认证访问测试

- **订单模块测试** (`apps/orders/tests.py`)
  - 订单CRUD操作
  - 订单状态更新
  - 订单项管理
  - 订单隔离（用户只能访问自己的订单）
  - 数据验证测试

- **用户模块测试** (`apps/users/tests.py`)
  - 管理员权限测试
  - 普通用户权限测试

### 注意事项

1. 首次运行需要执行数据库迁移
2. 需要创建用户账号才能登录系统
3. 数据库数据会持久化在Docker Volume中
4. 修改代码后需要重启容器才能生效（或使用volume挂载进行开发）
5. 所有API接口都有对应的测试用例，确保功能正常
