import os
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.user.daos.user_dao import UserDAO
from app.modules.user.schemas.user import UserCreate, UserUpdate

class UserService:
    def __init__(self, db: AsyncSession):
        self.dao = UserDAO(db)

    async def update_user_properties(self, user_id: int, update_data: UserUpdate):
        return await self.dao.update_user(user_id, update_data)

    async def get_user_by_id(self, user_id: int):
        return await self.dao.get_user_by_id(user_id)

    async def get_user_by_email(self, email: str):
        return await self.dao.get_user_by_email(email)

    async def create_user(self, user_data: UserCreate):
        return await self.dao.create_user(user_data)

    async def update_user_avatar(self, uid, file, filename):
        _, file_extension = os.path.splitext(filename)
        filename: str = f'avatar_{uid}_avatar{file_extension}'
        
        save_path = os.path.join("static", "avatars")
        os.makedirs(save_path, exist_ok=True)
        file_location = os.path.join(save_path, filename)
        
        with open(file_location, "wb+") as file_object:
            file_object.write(file.read())
        return filename





