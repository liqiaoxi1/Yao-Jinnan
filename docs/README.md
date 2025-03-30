# API 文档

## 目录
1. [用户模块](#用户模块)
2. [任务模块](#任务模块)
3. [日报模块](#日报模块)

## 用户模块

### 数据模型

#### LoginForm
登录表单模型

##### 字段
| 字段名 | 类型 | 描述 |
|--------|------|------|
| mobile | str | 手机号，最大长度11位 |
| password | str | 密码 |
| method | str | 登录方式: 0=密码, 1=短信 |

#### UserCreate
用户创建模型

##### 字段
| 字段名 | 类型 | 描述 |
|--------|------|------|
| mobile | str | 手机号，最大长度11位 |
| password | str | 密码 |
| nickname | Optional[str] | 昵称 |
| email | Optional[EmailStr] | 邮箱 |

#### UserUpdate
用户信息更新模型

##### 字段
| 字段名 | 类型 | 描述 |
|--------|------|------|
| mobile | Optional[str] | 手机号，最大长度11位 |
| email | Optional[EmailStr] | 邮箱 |
| nickname | Optional[str] | 昵称，最大长度50位 |
| gender | Optional[int] | 性别: 0=未知, 1=男, 2=女 |
| avatar | Optional[str] | 头像URL |
| birthday | Optional[date] | 生日 |
| status | Optional[str] | 状态，最大长度30位 |

#### UserSchema
用户信息模型

##### 字段
| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | int | 用户ID |
| uid | str | 用户唯一标识 |
| mobile | str | 手机号 |
| nickname | str | 昵称 |
| email | Optional[str] | 邮箱 |
| avatar | str | 头像URL |
| gender | int | 性别: 0=未知, 1=男, 2=女 |
| birthday | Optional[date] | 生日 |
| status | str | 状态 |
| last_login_time | Optional[datetime] | 最后登录时间 |
| last_login_ip | Optional[str] | 最后登录IP |
| create_time | datetime | 创建时间 |
| update_time | datetime | 更新时间 |
| password | Optional[str] | 密码 |

### API 接口

#### 用户认证

##### 登录
**请求方法**: POST
**路径**: /api/v1/login

登录接口支持密码登录和短信登录两种方式。

**请求参数**:
- mobile: 手机号
- password: 密码
- method: 登录方式（0=密码，1=短信）

**响应**:
```json
{
    "data": {
        "access_token": "访问令牌",
        "refresh_token": "刷新令牌",
        "token_type": "bearer"
    },
    "statusCode": 200
}
```

#### 用户注册

##### 注册新用户
**请求方法**: POST
**路径**: /api/v1/register

**请求参数**:
- mobile: 手机号
- password: 密码
- nickname: 昵称（可选）
- email: 邮箱（可选）

**响应**: 返回创建的用户信息

#### 用户信息

##### 获取用户信息
**请求方法**: GET
**路径**: /api/v1/user/info

**响应**: 返回当前登录用户的完整信息

##### 更新用户信息
**请求方法**: PATCH
**路径**: /api/v1/user/update

**请求参数**: 支持更新以下字段
- mobile: 手机号
- email: 邮箱
- nickname: 昵称
- gender: 性别
- avatar: 头像
- birthday: 生日
- status: 状态

**响应**: 返回更新后的用户信息

##### 更新用户头像
**请求方法**: POST
**路径**: /api/v1/user/avatar_update

**请求参数**:
- file: Base64编码的图片数据
- filename: 文件名

**响应**:
```json
{
    "code": 200,
    "message": "Avatar updated successfully",
    "data": {
        "url": "头像URL"
    }
}
```

##### 更新用户昵称
**请求方法**: PUT
**路径**: /api/v1/user/name_update

**请求参数**:
- nickname: 新昵称

**响应**: 返回更新后的用户信息

## 任务模块

### 数据模型

#### SubTask
子任务模型

##### 字段
| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | int | 子任务ID |
| title | str | 子任务标题 |
| status | str | 子任务状态 |

#### TaskBase
任务基础模型

##### 字段
| 字段名 | 类型 | 描述 |
|--------|------|------|
| name | str | 任务名称 |
| description | str | 任务描述 |

#### TaskCreate
任务创建模型

##### 字段
| 字段名 | 类型 | 描述 |
|--------|------|------|
| name | str | 任务名称 |
| description | str | 任务描述 |

#### TaskUpdate
任务更新模型

##### 字段
| 字段名 | 类型 | 描述 |
|--------|------|------|
| name | Optional[str] | 任务名称 |
| description | Optional[str] | 任务描述 |

#### Task
任务完整模型

##### 字段
| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | int | 任务ID |
| name | str | 任务名称 |
| description | str | 任务描述 |
| create_time | datetime | 创建时间 |
| update_time | datetime | 更新时间 |
| subtask | Optional[SubTask] | 子任务信息 |

### API 接口

#### 创建任务
**请求方法**: POST
**路径**: /api/v1/task/

**请求参数**:
- name: 任务名称
- description: 任务描述

**响应**: 返回创建的任务信息

#### 更新任务
**请求方法**: PUT
**路径**: /api/v1/task/{task_id}

**请求参数**:
- name: 任务名称（可选）
- description: 任务描述（可选）

**响应**: 返回更新后的任务信息

#### 获取任务详情
**请求方法**: GET
**路径**: /api/v1/task/{task_id}

**响应**: 返回指定任务的详细信息

#### 获取任务列表
**请求方法**: GET
**路径**: /api/v1/task/

**响应**: 返回所有任务列表

#### 删除任务
**请求方法**: DELETE
**路径**: /api/v1/task/{task_id}

**响应**: 返回被删除的任务信息

## 日报模块

### API 接口

#### 生成每日任务总结
**请求方法**: GET
**路径**: /api/v1/daily_report

**请求参数**:
- date: 目标日期，格式为 YYYY-MM-DD

**响应**:
```json
{
    "date": "YYYY-MM-DD",
    "summary": "任务总结内容"
}
```

#### 测试接口
**请求方法**: GET
**路径**: /api/v1/daily_report_test

**响应**: 返回当前用户ID和认证状态

## 错误处理

所有接口在发生错误时会返回适当的 HTTP 状态码和错误信息：

- 400: 请求参数错误
- 401: 未授权
- 404: 资源未找到
- 500: 服务器内部错误

## 更新日志

### 2024-03-30
- 初始版本
- 整合用户、任务和日报模块文档 