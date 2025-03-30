# 请求和登录、注册表单模型
import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr, Field, field_validator, model_validator, ConfigDict
from pydantic.networks import validate_email as pydantic_validate_email
from app.modules.user.models.user import User


class LoginForm(BaseModel):
    mobile: str = Field("18888888888", max_length=11)
    password: str = "123456"
    method: str = Field("0", description="登录方式: 0=密码, 1=短信")


class UserCreate(BaseModel):
    mobile: constr(strip_whitespace=True, max_length=11)
    password: str
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None


class UserAuthenticate(LoginForm):
    pass


class UserUpdate(BaseModel):
    mobile: Optional[constr(strip_whitespace=True, max_length=11)] = None
    email: Optional[EmailStr] = None
    nickname: Optional[str] = Field(None, max_length=50)
    gender: Optional[int] = Field(None, ge=0, le=2)
    avatar: Optional[str] = None
    birthday: Optional[datetime.date] = None
    status: Optional[str] = Field(None, max_length=30)


class LoginResult(BaseModel):
    status: bool
    msg: str
    user: Optional["UserSchema"] = None
    password:Optional[str]=None
    model_config = ConfigDict(from_attributes=True,arbitrary_types_allowed=True)


class UserSchema(BaseModel):
    id: int
    uid: str
    mobile: str
    nickname: str
    email: Optional[str] = None
    avatar: str
    gender: int = Field(0, ge=0, le=2, description="性别: 0=未知, 1=男, 2=女")
    birthday: Optional[datetime.date] = None
    status: str = Field("", max_length=30)
    last_login_time: Optional[datetime.datetime] = None
    last_login_ip: Optional[str] = None
    create_time: datetime.datetime
    update_time: datetime.datetime

    @field_validator('email')
    def validate_email(cls, v):
        if not v:
            return ""
        try:
            valid_email = pydantic_validate_email(v)
            return valid_email[1]
        except ValueError:
            raise ValueError("无效的邮箱格式")

    model_config = ConfigDict(from_attributes=True,arbitrary_types_allowed=True)
