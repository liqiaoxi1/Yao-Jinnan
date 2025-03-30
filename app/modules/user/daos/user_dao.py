from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.modules.user.models.user import User
from app.modules.user.schemas.user import UserCreate, UserUpdate, UserAuthenticate
from core.exceptions import CustomException
from core.config import settings
import uuid # 用于生成唯一的 UUID

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 异步数据库操作，适用于高并发

class UserDAO:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_user_by_mobile(self, mobile: str):
        stmt = select(User).where(User.mobile == mobile)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_user_by_id(self, user_id: int):
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_user_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_user_by_uid(self, uid: str):
        stmt = select(User).where(User.uid == uid)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def save_user(self, user):
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def create_user(self, user_data: UserCreate):
        if await self.get_user_by_mobile(user_data.mobile):
            raise CustomException("用户已存在")
        hashed_password = pwd_context.hash(user_data.password or settings.DEFAULT_PASSWORD)
        # 生成8位唯一用户名：使用uuid4前8位，并确保唯一性
        uid = str(uuid.uuid4()).replace('-', '')[:8]
        # 检查uid是否已存在，如果存在则重新生成
        while await self.get_user_by_uid(uid):
            uid = str(uuid.uuid4()).replace('-', '')[:8]
            
        user = User(
            mobile=user_data.mobile,
            password=hashed_password,
            avatar=settings.DEFAULT_AVATAR,
            uid=uid
        )
        self.db.add(user)
        await self.db.commit()
        return user

    async def authenticate_user(self, auth_data: UserAuthenticate):
        user = await self.get_user_by_mobile(auth_data.mobile)
        # 密码哈希验证方法：验证原始密码是否与哈希密码一致
        if user and pwd_context.verify(auth_data.password, user.password):
            return user
        elif user:
            return -1  # 密码错误
        return None

    async def update_user(self, user_id: int, update_data: UserUpdate):
        user = await self.get_user_by_id(user_id)
        if user:
            update_data_dict = update_data.__dict__
            for key, value in update_data_dict.items():
                if value is not None:
                    setattr(user, key, value)
            await self.db.commit()
            return user
        return None

    async def delete_user(self, user_id: int):
        user = await self.get_user_by_id(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
