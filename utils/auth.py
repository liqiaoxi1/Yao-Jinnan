from fastapi import Depends, HTTPException, Security, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import settings
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
import jwt

from core.exceptions import CustomException
from starlette import status

security = HTTPBearer()

class Auth:
    def __init__(self, db: AsyncSession, user_info: dict):
        self.db = db
        self.user_info = user_info

async def get_auth(
    db: AsyncSession = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security)
) -> Auth:
    """
    解析并验证JWT，提取用户信息，同时提供数据库会话。
    """

    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if datetime.fromtimestamp(payload['exp']) < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="认证已失效，请您重新登录")
        return Auth(db, payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="认证已失效，请您重新登录")
    except (jwt.InvalidSignatureError, jwt.DecodeError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无效认证，请您重新登录")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during authentication")



async def websocket_auth(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db)
) -> Auth:
    """
    在 WebSocket 连接中解析并验证 JWT，提取用户信息，同时提供数据库会话。
    """
    await websocket.accept()  # 先接受连接

    try:
        # 从 WebSocket 连接的查询参数中获取 token
        token = websocket.query_params.get("token")

        if not token:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="缺少认证令牌")

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if datetime.fromtimestamp(payload['exp']) < datetime.utcnow():
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="认证已失效，请您重新登录")

        # 构造 Auth 对象
        return Auth(db, payload)

    except jwt.ExpiredSignatureError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="认证已失效，请您重新登录")
    except (jwt.InvalidSignatureError, jwt.DecodeError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无效认证，请您重新登录")
    except Exception as e:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

async def get_user_id(auth: Auth = Depends(get_auth)):
    user_id = auth.user_info.get('sub', None)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user_id