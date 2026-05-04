# Web认证机制详解：Session、Token(JWT)、Cookie

## 目录

1. [什么是认证(Authentication)](#1-什么是认证)
2. [Cookie 详解](#2-cookie-详解)
3. [Session 详解](#3-session-详解)
4. [Token(JWT) 详解](#4-tokenjwt-详解)
5. [三种方式对比](#5-三种方式对比)
6. [本项目中的实现](#6-本项目中的实现)
7. [认证安全对比与攻击演示](#7-认证安全对比与攻击演示)
8. [常见安全问题](#8-常见安全问题)

***

<br />

核心问题：**如何让服务器知道当前请求是哪个用户发出的？**

## 1. 什么是认证

**认证(Authentication)** 是验证"你是谁"的过程。在Web应用中，HTTP协议是无状态的，每次请求都是独立的，服务器不会记住上一次请求是谁发的。因此需要一种机制来"记住"用户身份。

三种主流解决方案：

- **Session**：服务端记住你是谁
- **Token**：你带着证明你是谁
- **Cookie**：浏览器帮你带着证明

***

## 2. Cookie 详解

### 2.1 什么是Cookie

Cookie是浏览器存储在用户电脑上的小段文本数据（最大4KB）。每次HTTP请求，浏览器会自动携带匹配的Cookie。

### 2.2 Cookie的工作流程

```
1. 浏览器发送请求 → 服务器
2. 服务器通过 Set-Cookie 响应头设置Cookie
   Set-Cookie: username=zhangsan; Max-Age=604800; Path=/
3. 浏览器自动保存Cookie
4. 后续请求浏览器自动携带Cookie
   Cookie: username=zhangsan
5. 服务器从请求的Cookie中读取数据
```

### 2.3 Cookie的重要属性

| 属性           | 说明                            | 安全作用            |
| ------------ | ----------------------------- | --------------- |
| **HttpOnly** | 设为true时，JavaScript无法读取此Cookie | 防止XSS攻击窃取Cookie |
| **Secure**   | 设为true时，仅通过HTTPS传输            | 防止中间人攻击         |
| **SameSite** | 控制跨站请求是否携带Cookie              | 防止CSRF攻击        |
| **Max-Age**  | Cookie过期时间（秒）                 | 控制Cookie有效期     |
| **Domain**   | Cookie所属域名                    | 限制Cookie作用范围    |
| **Path**     | Cookie生效的URL路径                | 限制Cookie作用路径    |

### 2.4 SameSite属性详解

```
SameSite=Strict  → 完全禁止跨站携带，最安全但影响体验
SameSite=Lax     → 允许顶级导航的GET请求携带（默认值，推荐）
SameSite=None    → 允许跨站携带（必须同时设置Secure）
```

### 2.5 Cookie在本项目中的用途

```python
# 后端设置Cookie（users/views.py - CookieLoginView）
response.set_cookie(
    key='access_token',        # Cookie名称
    value=access_token,        # Cookie值（JWT Token）
    httponly=True,             # JS无法读取，防XSS
    secure=False,              # 开发环境False，生产必须True
    samesite='Lax',            # 防CSRF
    max_age=3600,              # 1小时过期
)
```

```typescript
// 前端读取Cookie（utils/cookie.ts）
// 注意：HttpOnly的Cookie无法通过JS读取！
export function getCookie(name: string): string {
  const cookies = document.cookie.split(';')
  // 只能读取非HttpOnly的Cookie
}
```

***

## 3. Session 详解

### 3.1 什么是Session

Session是服务端存储的会话数据。服务器为每个用户创建一个Session对象，通过SessionID来标识。

### 3.2 Session的工作流程

```
1. 用户提交用户名密码
2. 服务器验证通过，创建Session对象（存储在数据库/缓存/文件中）
   Session = { session_key: "abc123", user_id: 1, ... }
3. 服务器通过Set-Cookie返回sessionid
   Set-Cookie: sessionid=abc123
4. 浏览器自动保存sessionid Cookie
5. 后续请求浏览器自动携带sessionid
   Cookie: sessionid=abc123
6. 服务器根据sessionid查找Session → 识别用户
```

### 3.3 Session的存储位置

Django支持多种Session存储后端：

```python
# 数据库存储（默认）
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# 缓存存储（推荐生产环境）
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# 文件存储
SESSION_ENGINE = 'django.contrib.sessions.backends.file'

# Cookie存储（Session数据加密后存在Cookie中，不推荐）
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
```

### 3.4 Session的关键配置

```python
# settings.py
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7     # Session有效期：7天
SESSION_COOKIE_NAME = 'studyhub_sessionid'  # Cookie名称
SESSION_COOKIE_HTTPONLY = True              # 防止JS读取
SESSION_COOKIE_SAMESITE = 'Lax'             # 防止CSRF
SESSION_SAVE_EVERY_REQUEST = False          # 不每次请求都保存（避免切换认证方式时Session被重新保存）
```

### 3.5 Session在本项目中的实现

```python
# 后端Session登录（users/views.py - SessionLoginView）
from django.contrib.auth import login, authenticate

def post(self, request):
    user = authenticate(request, username=username, password=password)
    if user:
        # login()完成两件事：
        # 1. 在服务端创建Session（存入数据库）
        # 2. 在响应中设置Set-Cookie: sessionid=xxx
        login(request, user)
```

```typescript
// 前端无需手动处理Session
// 浏览器自动携带sessionid Cookie
// 只需确保 axios 设置 withCredentials: true
const http = axios.create({
  withCredentials: true,  // 跨域时携带Cookie（包括sessionid）
})
```

***

## 4. Token(JWT) 详解

### 4.1 什么是JWT

JWT(JSON Web Token)是一种开放标准(RFC 7519)，用于在各方之间安全地传输信息。JWT是一个加密的字符串，包含用户信息，无需服务端存储。

### 4.2 JWT的结构

JWT由三部分组成，用`.`分隔：

```
xxxxx.yyyyy.zzzzz
│     │     └── Signature（签名）
│     └──────── Payload（载荷/数据）
└────────────── Header（头部）
```

**Header（头部）**：

```json
{
  "alg": "HS256",   // 签名算法
  "typ": "JWT"      // 令牌类型
}
```

**Payload（载荷）**：

```json
{
  "user_id": 1,           // 用户ID
  "exp": 1700000000,      // 过期时间
  "iat": 1699996400,      // 签发时间
  "token_type": "access"  // Token类型
}
```

**Signature（签名）**：

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key  // 服务端密钥
)
```

### 4.3 JWT的工作流程

```
1. 用户提交用户名密码
2. 服务器验证通过，生成JWT Token
   access_token = 短期令牌（如60分钟）
   refresh_token = 长期令牌（如7天）
3. 服务器返回Token给前端（不通过Cookie，直接在响应体中）
4. 前端将Token存储到localStorage
5. 后续请求在Authorization头中携带Token
   Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
6. 服务器验证Token签名和有效期 → 识别用户
```

### 4.4 双Token机制

```
access_token  → 短期有效（如60分钟），用于日常请求
refresh_token → 长期有效（如7天），用于刷新access_token

流程：
1. 登录获取 access_token + refresh_token
2. 请求时使用 access_token
3. access_token过期 → 401错误
4. 用 refresh_token 请求新的 access_token
5. refresh_token也过期 → 需要重新登录
```

### 4.5 JWT在本项目中的实现

```python
# 后端Token登录（users/views.py - TokenLoginView）
from rest_framework_simplejwt.tokens import RefreshToken

def post(self, request):
    user = authenticate(request, username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),   # 短期Token
            'refresh': str(refresh),                # 长期Token
        })
```

```typescript
// 前端Token处理（utils/request.ts）

// 1. 登录时存储Token
localStorage.setItem('access_token', response.data.access)
localStorage.setItem('refresh_token', response.data.refresh)

// 2. 请求拦截器自动添加Token
http.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 3. Token过期自动刷新
http.interceptors.response.use(null, async (error) => {
  if (error.response?.status === 401) {
    const refreshToken = localStorage.getItem('refresh_token')
    const res = await axios.post('/api/auth/token/refresh/', { refresh: refreshToken })
    localStorage.setItem('access_token', res.data.access)
  }
})
```

***

## 5. 三种方式对比

### 5.1 核心对比表

| 对比项       | Session           | Token(JWT)        | Cookie      |
| --------- | ----------------- | ----------------- | ----------- |
| **存储位置**  | 服务端               | 客户端(localStorage) | 浏览器Cookie   |
| **传输方式**  | Cookie(sessionid) | Authorization头    | Cookie      |
| **状态**    | 有状态               | 无状态               | 无状态         |
| **服务端存储** | 需要                | 不需要               | 不需要         |
| **扩展性**   | 差(需共享Session)     | 好(无状态)            | 好(无状态)      |
| **安全性**   | 较高(需配合SameSite)   | 较高(XSS风险)         | 取决于配置       |
| **撤销**    | 容易(删Session)      | 困难(等过期)           | 容易(清Cookie) |
| **跨域**    | 困难                | 容易                | 需配置         |
| **大小限制**  | 无(服务端存储)          | 无                 | 4KB         |
| **移动端**   | 不友好               | 友好                | 不友好         |
| **CSRF防护** | 🟡 SameSite部分防护   | ✅ 天然免疫            | 🟡 SameSite部分防护 |

### 5.2 安全性对比

| 攻击类型     | Session         | Token                | Cookie(HttpOnly)         |
| -------- | --------------- | -------------------- | ------------------------ |
| **XSS**  | sessionid可被JS读取 | Token可被JS读取          | HttpOnly的Cookie无法被JS读取 ✅ |
| **CSRF** | 🟡 SameSite部分防护   | 不受影响(Token在Header) ✅ | 🟡 SameSite部分防护            |
| **中间人**  | 需HTTPS          | 需HTTPS               | 需HTTPS + Secure属性        |

### 5.3 适用场景

- **Session**：传统Web应用，服务端渲染，单体架构
- **Token(JWT)**：前后端分离，SPA应用，微服务架构，移动端
- **Cookie**：需要浏览器自动管理Token，兼顾安全性和便利性

***

## 6. 本项目中的实现

### 6.1 项目结构

```
StudyHub/
├── backend/                    # Django后端
│   ├── config/                 # 项目配置
│   │   ├── settings.py         # 包含Session/JWT/Cookie配置
│   │   └── urls.py             # 路由入口
│   ├── users/                  # 用户应用（认证核心）
│   │   ├── views.py            # 三种认证方式的视图
│   │   ├── urls.py             # 认证路由
│   │   └── models.py           # 用户模型
│   └── posts/                  # 帖子应用（受保护的资源）
│       ├── views.py            # 帖子CRUD + 点赞/收藏/评论
│       ├── serializers.py      # 帖子序列化器
│       ├── models.py           # 帖子、评论、点赞、收藏模型
│       └── urls.py             # 帖子路由
├── frontend/                   # Vue3前端
│   └── src/
│       ├── api/                # API封装
│       │   ├── auth.ts         # 三种认证API
│       │   └── posts.ts        # 帖子API
│       ├── utils/              # 工具函数
│       │   ├── request.ts      # Axios封装（Token拦截器）
│       │   └── cookie.ts       # Cookie操作工具
│       ├── store/              # 状态管理
│       │   └── user.ts         # 用户状态（认证信息）
│       └── views/              # 页面
│           ├── LoginView.vue            # 登录页（三种方式）
│           ├── RegisterView.vue         # 注册页
│           ├── HomeView.vue             # 首页（帖子列表）
│           ├── PostDetailView.vue       # 帖子详情页
│           ├── PostProcessView.vue      # 帖子发布流程演示
│           ├── MyContentView.vue        # 我的内容（帖子/收藏/草稿）
│           ├── ProfileView.vue          # 个人中心
│           ├── AuthProcessView.vue      # 认证流程演示
│           ├── AuthSecurityView.vue     # 认证安全对比
│           └── AttackProcessView.vue    # 攻击演示动画
└── docs/                       # 文档
    └── auth_guide.md           # 本文档
```

### 6.2 API路由

| 路由                             | 认证方式          | 说明            |
| ------------------------------ | ------------- | ------------- |
| POST /api/auth/register/       | 全部            | 注册（邮箱选填）     |
| POST /api/auth/session/login/  | Session       | Session登录     |
| POST /api/auth/session/logout/ | Session       | Session登出     |
| POST /api/auth/token/login/    | Token         | Token登录       |
| POST /api/auth/token/refresh/  | Token         | 刷新Token       |
| POST /api/auth/cookie/login/   | Cookie        | Cookie登录      |
| POST /api/auth/cookie/logout/  | Cookie        | Cookie登出      |
| GET /api/posts/                | 只读(列表)        | 帖子列表（搜索+分页）  |
| POST /api/posts/               | 需要认证          | 创建帖子/保存草稿    |
| GET /api/posts/{id}/           | 只读            | 帖子详情（自动计数浏览量）|
| PUT /api/posts/{id}/           | 需要认证（仅作者）    | 更新帖子/发布草稿    |
| DELETE /api/posts/{id}/        | 需要认证（仅作者）    | 删除帖子          |
| POST /api/posts/{id}/like/     | 需要认证          | 点赞/取消点赞      |
| POST /api/posts/{id}/favorite/ | 需要认证          | 收藏/取消收藏      |
| GET /api/posts/my_posts/       | 需要认证          | 我的帖子          |
| GET /api/posts/my_favorites/   | 需要认证          | 我的收藏          |
| GET /api/posts/my_drafts/      | 需要认证          | 我的草稿          |
| GET /api/posts/{id}/comments/  | 只读            | 帖子评论列表       |
| POST /api/posts/{id}/comments/ | 需要认证          | 发表评论          |
| PUT /api/posts/{id}/comments/{cid}/ | 需要认证（仅作者） | 编辑评论          |
| DELETE /api/posts/{id}/comments/{cid}/ | 需要认证（仅作者） | 删除评论          |

### 6.3 学习建议

1. **先注册账号**，体验三种认证同时初始化
2. **分别用三种方式登录**，观察请求和响应的差异：
   - Session：查看Set-Cookie中的sessionid
   - Token：查看响应体中的access_token和refresh_token
   - Cookie：查看Set-Cookie中的access_token
3. **打开浏览器开发者工具**：
   - Application → Cookies：查看Cookie
   - Application → Local Storage：查看Token
   - Network：查看请求头中的Authorization和Cookie
4. **访问认证安全对比页面** (`/auth-security`)，查看三种认证在不同攻击下的表现
5. **体验攻击演示动画** (`/attack-process`)，了解XSS、CSRF、凭证泄露的攻击过程和防御方案
6. **阅读代码注释**，理解每种认证方式的实现细节

***

## 7. 认证安全对比与攻击演示

### 7.1 XSS（跨站脚本攻击）

**攻击原理**：攻击者注入恶意JavaScript代码到网页中，当其他用户访问时，恶意脚本在其浏览器中执行。

**三种认证受影响情况**：

| 认证方式 | 受影响程度 | 说明 |
|---------|---------|------|
| Session | 🟡 部分防护 | HttpOnly防止JS读取sessionid，但攻击者仍可通过XSS直接发请求冒充用户 |
| Token | 🔴 高危 | localStorage中的Token可被JS直接读取，攻击者可轻松窃取 |
| Cookie | ✅ 安全 | HttpOnly Cookie完全无法被JS读取，即使存在XSS也无法窃取 |

### 7.2 CSRF（跨站请求伪造）

**攻击原理**：攻击者诱导用户访问恶意网站，利用浏览器自动携带Cookie的特性，伪造用户请求。

**三种认证受影响情况**：

| 认证方式 | 受影响程度 | 说明 |
|---------|---------|------|
| Session | 🟡 部分防护 | SameSite=Lax阻止跨站POST请求携带Cookie，但GET请求仍可能携带 |
| Token | ✅ 安全 | Authorization头不会被浏览器自动携带，天然免疫CSRF |
| Cookie | 🟡 部分防护 | 与Session完全一致，POST被阻止但GET仍可能携带 |

**SameSite=Lax的局限性**：
- ✅ 阻止跨站POST请求（如恶意表单提交）
- ⚠️ 不阻止跨站GET请求（如`<img src="银行转账URL">`）
- 如需完全防护，建议使用CSRF Token机制

### 7.3 凭证泄露

**攻击原理**：攻击者通过网络嗅探、日志泄露等途径获取用户的认证凭证。

**三种认证受影响情况**：

| 认证方式 | 受影响程度 | 说明 |
|---------|---------|------|
| Session | 🟢 可即时撤销 | 管理员可删除服务端Session，立即失效 |
| Token | 🔴 无法撤销 | JWT Token在过期前一直有效，只能等过期 |
| Cookie | 🟡 部分可控 | 可删除Cookie，但服务端Token仍有效直到过期 |

***

## 8. 常见安全问题

### 8.1 XSS（跨站脚本攻击）

**攻击方式**：注入恶意JS代码，窃取Cookie或Token

**防护措施**：

- Cookie设置 `HttpOnly=True`（JS无法读取）
- Token存储在HttpOnly Cookie中而非localStorage
- 对用户输入进行转义/过滤
- 设置Content-Security-Policy头

### 8.2 CSRF（跨站请求伪造）

**攻击方式**：诱导用户访问恶意网站，利用已登录的Cookie发起请求

**防护措施**：

- Cookie设置 `SameSite=Lax` 或 `Strict`
- 使用CSRF Token双重验证（更严格）
- Token认证不受CSRF影响（Token在Header中，不在Cookie中）
- 验证Referer/Origin头

### 8.3 Token泄露

**防护措施**：

- 使用HTTPS传输
- 设置合理的Token过期时间
- access_token短期有效
- Token存储在HttpOnly Cookie中
- 及时刷新refresh_token
