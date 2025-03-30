## FastAPI Project Template

这是一个基于FastAPI框架的现代化Python Web项目模板，采用最佳实践和清晰的项目结构。

### 🎯 特性

- 🚀 FastAPI 框架
- 🔐 JWT认证
- 🗃️ SQLAlchemy ORM
- 🔄 数据库迁移(Alembic)
- ⚡ 异步支持（asyncio，异步数据库连接及dao）
- 🧪 单元测试 
- 📝 代码规范分层架构，通过构造函数注入依赖（如数据库会话）
- 🐳 Docker支持

### 🚀 快速开始

#### 环境要求

- Python 3.9+
- MySQL 5.7+ / PostgreSQL 12+
- Docker (可选)

#### 1. 克隆项目

```bash
git clone <your-repository-url>
cd <project-name>
```

#### 2. 配置环境

推荐使用conda创建虚拟环境:

```bash
# 使用配置文件创建环境
conda env create -f environment.yml

# 或手动创建
conda create -n myproject python=3.9
conda activate myproject
pip install -r requirements.txt
```

#### 3. 配置数据库

##### MySQL配置步骤

1. 确保本地MySQL服务已启动
2. 使用MySQL命令行或图形化工具(如Navicat、MySQL Workbench)连接到MySQL
3. 创建新数据库，注意选择正确的字符集：
```sql
CREATE DATABASE your_database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

4. 配置数据库连接信息：
   - 打开项目根目录下的`.env`文件
   - 修改以下数据库相关配置：
```env
DB_USER=your_username        # MySQL用户名
DB_PASSWORD=your_password    # MySQL密码
DB_HOST=localhost           # 数据库主机地址
DB_PORT=3306               # MySQL端口号
DB_NAME=your_database_name # 上一步创建的数据库名
```

##### 使用Docker启动MySQL (推荐)

```bash
# 拉取MySQL镜像
docker pull mysql:5.7

# 启动容器
docker run -d \
  --name project-mysql \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=your_password \
  mysql:5.7
```

#### 4. 配置环境变量

在项目根目录创建`.env`文件:

```env
# API配置
API_VERSION=1.0.0
ENV=dev
ALLOWED_HOSTS=["localhost", "localhost:8000"]

# 数据库配置
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=dbname

# JWT配置
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### 5. 数据库迁移

```bash
# 初始化迁移
alembic init alembic

# 创建迁移脚本
alembic revision --autogenerate -m "init"

# 执行迁移
alembic upgrade head
```

#### 6. 启动服务

```bash
# 开发模式
uvicorn main:app --host 0.0.0.0 --reload   # 默认8000端口
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


# 生产模式
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

访问 http://localhost:8000/docs 查看API文档

### 📦 项目结构

```
fastapi-template/
├── app/                    # 应用主目录
│   ├── api/               # API路由
│   ├── core/              # 核心配置
│   ├── crud/              # 数据库操作
│   ├── db/                # 数据库配置
│   ├── models/            # 数据库模型
│   ├── schemas/           # Pydantic模型
│   └── utils/             # 工具函数
├── tests/                 # 测试用例
├── alembic/              # 数据库迁移
├── static/               # 静态文件
├── .env                  # 环境变量
├── main.py              # 应用入口
└── requirements.txt     # 项目依赖
```

models：数据模型层
schemas：数据验证层
daos：数据访问层
services：业务逻辑层
api：接口层

### 🧪 运行测试

```bash
pytest
```

### 🐳 Docker部署

```bash
# 构建镜像
docker build -t fastapi-app .

# 运行容器
docker run -d -p 8000:8000 fastapi-app
```

### 📝 开发指南

#### 代码规范
- 遵循PEP8规范
- 使用Black格式化代码
- 编写单元测试

#### Git工作流
1. 创建功能分支
2. 提交代码
3. 运行测试
4. 发起Pull Request

#### 实训感想
本次实训我从零开始动手搭建了一个完整的FastAPI项目，过程中不仅学习了框架的使用，更深入理解了接口开发、调试、文档生成和部署的实际流程。
最开始我基于 FastAPI 框架实现了任务系统的接口，包括task的增删改查功能，子关联表的创建及查询的实现，还新增了一个“生成日报总结”的接口，这个接口集成了 Langchain 和智谱GLM模型，用来根据指定日期汇总当天的已完成任务并生成总结。过程中我熟悉了API路由、依赖注入、服务层调用大模型并写入数据库等代码。
开发完成后，我又使用Swagger和Apifox对接口进行了调试。文档部分，我通过Cursor编辑器整理接口markdown文档，把API层和schema层的内容生成标准接口说明文件，放进docs文件夹。最后，我将本地项目上传到了GitHub。这次实训帮助我全面掌握了FastAPI项目从开发到部署的关键技能，为我对后端开发的框架理解与技术学习都助力许多。
