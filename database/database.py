# app/database/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import create_engine
from database.base_class import Base

# 使用 Async 引擎和 MySQL 的异步 URL 格式
# 创建异步的 SQLAlchemy engine
async_engine = create_async_engine(
    "mysql+aiomysql://" +
    settings.DB_USER + ":" +
    settings.DB_PASSWORD + "@" +
    settings.DB_HOST + ":" +
    str(settings.DB_PORT) + "/" +
    settings.DB_NAME, echo=True,
    pool_size=20,          # 设置连接池的大小
    max_overflow=10,      # 允许的最大溢出连接数
    pool_timeout=30,      # 连接池超时时间
    pool_pre_ping=True     # 在获取连接之前测试连接是否可用
)

DATABASE_URL_ASYNC = f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{str(settings.DB_PORT)}/{settings.DB_NAME}"

# 同步
DATABASE_URL_SYNC = f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{str(settings.DB_PORT)}/{settings.DB_NAME}"


# 创建一个独立的同步引擎，仅供 langchain 使用
engine_sync = create_engine(DATABASE_URL_SYNC)


# 为同步操作创建一个单独的会话管理
SessionLocalSync = sessionmaker(autocommit=False, autoflush=True, bind=engine_sync)



# 创建异步的 sessionmaker
async_session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """
    Initialize the database by creating tables.
    """
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("数据库表创建成功")
    except Exception as e:
        print(f"创建数据库表时出错: {e}")

async def get_db():
    """
        get db session in async way
    """
    async with async_session_local() as session:
        yield session

def get_db_sync():
    """
    获取同步的 db session 并在异步环境中安全运行。
    """
    db = SessionLocalSync()
    try:
        yield db
    finally:
        db.close()
