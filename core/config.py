# app/core/config.py
"""
集中了 FastAPI 应用程序所需的各种设置，从环境变量或".env"文件加载的
"""
from pydantic_settings import BaseSettings
from core.path_conf import BasePath

class Settings(BaseSettings):
    API_VERSION: str = "1.0.0"
    CONTACT: dict = {  # Contact information
        "name": "FastAPI APP",
        "url": "https://example.com",
        "email": "contact@example.com",
    }
    ENV: str = "dev"
    if ENV == "dev":
        RELOAD: bool = True
        LOG_LEVEL: str = "debug"
    else:
        RELOAD: bool = False
        LOG_LEVEL: str = "info"

    ALLOWED_HOSTS: list = ["*"]

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DEBUG: bool

    DEFAULT_PASSWORD: str = "12345678"
    DEFAULT_AVATAR: str = ""

    """安全的随机密钥，该密钥将用于对 JWT 令牌进行签名"""
    SECRET_KEY: str
    """用于设定 JWT 令牌签名算法"""
    ALGORITHM: str = "HS256"
    """access_token 过期时间，一天"""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    """refresh_token 过期时间，用于刷新token使用，两天"""
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440 * 2

    ZHIPUAI_API_KEY: str
    SLEEP_TIME: float = 0.005
    """ Fake Streaming """


    class Config:
        env_file = f'{BasePath}/.env'  # 指定".env"文件的位置，该文件可能包含敏感信息，如数据库凭据。
        extra = "ignore"  # 指定".env"文件的位置，该文件可能包含敏感信息，如数据库凭据。

settings = Settings()



