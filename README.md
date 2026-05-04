# StudyHub - Web认证机制学习平台

一个用于学习和对比 **Session**、**Token(JWT)**、**Cookie** 三种Web认证方式的教学项目。

## 项目简介

StudyHub 是一个学习交流平台，核心特色是**同时实现了三种主流认证机制**，让开发者能够直观地理解它们的差异、优缺点和安全特性。

### 三种认证方式对比

| 对比项 | Session | Token(JWT) | Cookie |
|--------|---------|------------|--------|
| 存储位置 | 服务端 | 客户端(localStorage) | 浏览器Cookie |
| 传输方式 | Cookie(sessionid) | Authorization头 | Cookie |
| 状态 | 有状态 | 无状态 | 无状态 |
| CSRF防护 | 🟡 SameSite部分防护 | ✅ 天然免疫 | 🟡 SameSite部分防护 |
| XSS防护 | 🟡 HttpOnly防护 | 🔴 Token可被JS读取 | ✅ HttpOnly防护 |

## 功能特性

- 用户注册/登录/登出
- 三种认证方式独立切换
- 帖子发布/编辑/删除/草稿
- 帖子点赞/收藏
- 评论功能
- 认证流程可视化演示
- 安全攻击动画演示（XSS/CSRF/凭证泄露）

## 技术栈

### 后端
- Python 3.12+
- Django 4.2+
- Django REST Framework
- djangorestframework-simplejwt (JWT认证)
- django-cors-headers (跨域支持)
- MySQL (生产环境) / SQLite (开发环境)

### 前端
- Vue 3 + TypeScript
- Vite
- Pinia (状态管理)
- Vue Router
- Ant Design Vue
- Axios

## 项目结构

```
StudyHub/
├── backend/                    # Django后端
│   ├── config/                 # 项目配置
│   ├── users/                  # 用户认证模块
│   └── posts/                  # 帖子模块
├── frontend/                   # Vue3前端
│   └── src/
│       ├── api/                # API封装
│       ├── utils/              # 工具函数
│       ├── store/              # 状态管理
│       └── views/              # 页面组件
└── docs/                       # 文档
    ├── auth_guide.md           # 认证机制详解
    └── apifox_studyhub_api.json # API文档(OpenAPI 3.0)
```

## 快速开始

### 环境要求

- Python 3.12+
- Node.js 18+
- npm 或 yarn

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 启动服务
python manage.py runserver
```

后端运行在 http://localhost:8000

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端运行在 http://localhost:5173

### 环境变量配置

复制 `.env.example` 为 `.env` 并修改：

```bash
cp .env.example .env
```

| 变量 | 说明 | 默认值 |
|------|------|--------|
| DJANGO_SECRET_KEY | Django密钥 | 开发用默认值 |
| DEBUG | 调试模式 | True |
| ALLOWED_HOSTS | 允许的主机 | localhost,127.0.0.1 |

## API 文档

详细的API文档请参考 [docs/apifox_studyhub_api.json](docs/apifox_studyhub_api.json) (OpenAPI 3.0格式)

### 主要API端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/auth/register/` | POST | 用户注册 |
| `/api/auth/session/login/` | POST | Session登录 |
| `/api/auth/token/login/` | POST | Token登录 |
| `/api/auth/cookie/login/` | POST | Cookie登录 |
| `/api/posts/` | GET/POST | 帖子列表/创建 |
| `/api/posts/{id}/` | GET/PUT/DELETE | 帖子详情/更新/删除 |

## 学习资源

- [认证机制详解](docs/auth_guide.md) - Session/Token/Cookie 详细对比
- 认证流程演示页面：`/auth-process`
- 安全对比页面：`/auth-security`
- 攻击演示页面：`/attack-process`

## 生产环境部署

### 1. 环境变量配置

复制 `.env.example` 为 `.env` 并修改：

```bash
cp .env.example .env
```

生产环境必须修改的变量：

```env
DJANGO_SECRET_KEY=生成一个50位随机字符串
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 2. MySQL 数据库配置

```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=studyhub
DB_USER=studyhub_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=3306
```

创建数据库和用户：

```sql
CREATE DATABASE studyhub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'studyhub_user'@'localhost' IDENTIFIED BY 'your-secure-password';
GRANT ALL PRIVILEGES ON studyhub.* TO 'studyhub_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 部署步骤

```bash
# 后端
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic

# 使用 Gunicorn 启动
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# 前端
cd frontend
npm install
npm run build
# 将 dist 目录部署到 Nginx
```

### 4. Nginx 配置示例

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        root /path/to/studyhub/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

### 5. 安全检查清单

| 项目 | 要求 |
|------|------|
| `DEBUG` | `False` |
| `SECRET_KEY` | 强随机密钥 |
| `HTTPS` | 必须启用 |
| `SESSION_COOKIE_SECURE` | `True` |
| `CSRF_COOKIE_SECURE` | `True` |
| `CORS_ALLOW_ALL_ORIGINS` | `False` |

## License

MIT License
