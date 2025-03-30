# API 接口文档模板

## 文档信息

- **版本**: v1.0.0
- **更新日期**: YYYY-MM-DD
- **作者**: [作者名称]
- **状态**: [草稿/已审核/已发布]

## 目录

- [通用说明](接口说明.md#通用说明)
- [认证机制](接口说明.md#认证机制)
- [API端点](接口说明.md#api端点)
- [错误码](接口说明.md#错误码)
- [数据模型](接口说明.md#数据模型)
- [更新日志](接口说明.md#更新日志)

## 通用说明

### 基础信息

- **基础URL**: `https://api.example.com/v1`
- **数据格式**: JSON
- **字符编码**: UTF-8
- **时间格式**: ISO 8601 (YYYY-MM-DDTHH:mm:ssZ)

### 请求格式

```http
Content-Type: application/json
Accept: application/json
```

### 响应格式

所有API响应均遵循以下格式：

```json
{
    "code": 200,
    "message": "操作成功",
    "data": {
        // 具体的响应数据
    }
}
```

## 认证机制

### Bearer Token认证

#### HTTP接口
```http
Authorization: Bearer <access_token>
```

#### WebSocket接口
```
ws://your-domain/path?token=<access_token>
```

## API端点

### 模块：[模块名称]

#### 接口：[接口名称]

- **接口**: `/endpoint/path`
- **方法**: GET/POST/PUT/DELETE
- **描述**: [接口功能描述]

##### 请求参数

| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| param1 | string | 是 | 参数说明 | "example" |

##### 请求示例

```http
POST /api/endpoint HTTP/1.1
Content-Type: application/json

{
    "param1": "value1",
    "param2": "value2"
}
```

##### 响应参数

| 参数名 | 类型 | 描述 | 示例 |
|--------|------|------|------|
| field1 | string | 字段说明 | "example" |

##### 响应示例

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "field1": "value1",
        "field2": "value2"
    }
}
```

##### 错误响应

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 400 | 参数错误 | 检查请求参数 |

## 错误码

| 错误码 | 说明 | HTTP状态码 |
|--------|------|------------|
| 200 | 成功 | 200 |
| 400 | 请求参数错误 | 400 |
| 401 | 未授权 | 401 |
| 403 | 禁止访问 | 403 |
| 404 | 资源不存在 | 404 |
| 500 | 服务器内部错误 | 500 |

## 数据模型

### 模型名称

```json
{
    "field1": "类型：说明",
    "field2": "类型：说明"
}
```

## 更新日志

### v1.0.0 (YYYY-MM-DD)
- 初始版本发布
- [更新内容1]
- [更新内容2]

---

## 附录

### 常见问题

1. Q: [常见问题1]
   A: [解答1]

2. Q: [常见问题2]
   A: [解答2]

### 最佳实践

1. [最佳实践建议1]
2. [最佳实践建议2] 