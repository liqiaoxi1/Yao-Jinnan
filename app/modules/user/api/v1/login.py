from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
import app.modules.user.services.login_service as login_service
from app.modules.user.schemas.user import LoginForm
from database.database import get_db
from core.config import settings
from fastapi.responses import JSONResponse
from datetime import timedelta

router = APIRouter()

@router.post("/login", responses={200: {"description": "Token provided"}, 400: {"description": "Invalid request"}})
async def login_for_access_token(
    request: Request,
    data: LoginForm,
    db: AsyncSession = Depends(get_db)
):
    try:
        # 确定登录方法
        if data.method == "0":
            result = await login_service.password_login(data, db)
        elif data.method == "1":
            result = await login_service.sms_login(data, db)
        else:
            # 明确指出登录方法无效
            raise HTTPException(status_code=400, detail="Invalid user method provided.")

        # 处理登录失败情况
        if not result.status:
            raise HTTPException(status_code=401, detail=result.msg)

        # 生成和返回JWT (JSON Web Tokens) 创建JWT负载
        access_token = login_service.create_token(
            {"sub": result.user.id, "is_refresh": False, "password": result.password}
        )
        expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token = login_service.create_token(
            payload={"sub": result.user.id, "is_refresh": True, "password": result.password},
            expires=expires
        )

        resp = {
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            },
            "statusCode": status.HTTP_200_OK
        }

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=resp
        )

    except HTTPException as e:
        # 对于HTTP异常，返回HTTP异常的响应
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # 对于未预期的异常，返回通用错误响应
        if settings.DEBUG:
            print(e)  # 打印错误信息
        raise HTTPException(status_code=500, detail=str(e))