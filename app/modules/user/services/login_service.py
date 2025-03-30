from app.modules.user.schemas.user import UserAuthenticate, LoginResult
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.user.models.user import User
from app.modules.user.daos.user_dao import UserDAO
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from core.config import settings
from app.modules.user.schemas.user import UserSchema 
# 异步密码登录服务
async def password_login(form_data: UserAuthenticate, db: AsyncSession):
    user_dao = UserDAO(db)

    # 需要等待 get_user_by_mobile 方法返回的协程，然后才能使用 scalar_one_or_none 从查询中获取结果。
    user_result = await user_dao.authenticate_user(form_data)

    if user_result is None:
        return LoginResult(status=False, msg="用户不存在")

    elif user_result == -1:
        return LoginResult(status=False, msg="密码错误")

    return LoginResult(status=True, user=UserSchema.from_orm(user_result), msg="登录成功",password=user_result.password)

# 异步短信登录服务
async def sms_login(form_data: UserAuthenticate, db: AsyncSession):
    user = await User.get_user_by_mobile(db, form_data.mobile)


    if user is None:
        return {"status": False, "msg": "用户不存在"}

    # 检查短信验证码
    # 以下是模拟逻辑，实际逻辑应当访问Redis等存储来验证短信验证码
    if form_data.password != "1234":  # 假设用户输入的验证码是"1234"
        return {"status": False, "msg": "验证码错误"}

    return {"status": True, "msg": "登录成功"}


def create_token(payload: dict, expires: timedelta = None):
    """
    创建一个生成新的访问令牌的工具函数。

    pyjwt：https://github.com/jpadilla/pyjwt/blob/master/docs/usage.rst
    jwt 博客：https://geek-docs.com/python/python-tutorial/j_python-jwt.html

    """
    if expires:
        expire = datetime.utcnow() + expires
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt