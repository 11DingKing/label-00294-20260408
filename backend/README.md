# 订单管理系统 - 后端

基于 Django 4.2 + Django REST Framework 的订单管理后端服务。

## 技术栈

- Python 3.11
- Django 4.2
- Django REST Framework
- MySQL 8.0
- JWT 认证

## 目录结构

```
backend/
├── config/                 # 项目配置
│   ├── settings.py         # Django 设置
│   ├── urls.py             # 主路由
│   └── wsgi.py             # WSGI 配置
├── apps/                   # 应用模块
│   ├── authentication/     # 认证模块
│   ├── orders/             # 订单模块
│   └── users/              # 用户模块
├── utils/                  # 工具类
│   └── exceptions.py       # 全局异常处理
├── logs/                   # 日志目录
├── manage.py               # Django 管理脚本
├── requirements.txt        # Python 依赖
└── Dockerfile              # Docker 构建文件
```

## 本地开发

### 环境要求

- Python 3.11+
- MySQL 8.0+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置数据库

修改 `config/settings.py` 中的数据库配置，或设置环境变量：

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_NAME=order_management
export DB_USER=root
export DB_PASSWORD=your_password
```

### 数据库迁移

```bash
python manage.py migrate
```

### 创建管理员用户

```bash
python manage.py createsuperuser
```

### 启动开发服务器

```bash
python manage.py runserver 0.0.0.0:8000
```

## Docker 部署

```bash
docker build -t order-backend .
docker run -p 8010:8000 order-backend
```

## API 接口

### 认证接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/auth/login/ | 用户登录 |
| POST | /api/auth/logout/ | 用户退出 |
| GET | /api/auth/user/ | 获取当前用户 |
| POST | /api/auth/change-password/ | 修改密码 |

### 订单接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/orders/ | 获取订单列表 |
| POST | /api/orders/ | 创建订单 |
| GET | /api/orders/{id}/ | 获取订单详情 |
| PUT | /api/orders/{id}/ | 更新订单 |
| DELETE | /api/orders/{id}/ | 删除订单 |
| PATCH | /api/orders/{id}/status/ | 更新订单状态 |

## 运行测试

```bash
# 运行所有测试
python manage.py test apps.authentication apps.orders apps.users --verbosity=2

# 运行单个模块测试
python manage.py test apps.orders --verbosity=2
```

## 默认账号

- 用户名：admin
- 密码：admin123
