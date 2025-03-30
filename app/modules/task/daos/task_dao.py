from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.modules.task.models.task import Task

class TaskDao:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_task_by_id(self, task_id: int):
        result = await self.db.execute(
            select(Task).where(Task.id == task_id)
        )
        return result.scalar_one_or_none()

    async def get_task_by_name(self, name: str) -> Optional[Task]:
        result = await self.db.execute(
            select(Task).where(Task.name == name)
        )
        return result.scalar_one_or_none()

    async def get_all_tasks(self) -> List[Task]:
        result = await self.db.execute(select(Task))
        return result.scalars().all()

    async def create_task(self, task_data: dict):
        task = Task(**task_data)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def update_task(self, task_id: int, task_data: dict):
        task = await self.get_task_by_id(task_id)
        if task:
            for key, value in task_data.items():
                setattr(task, key, value)
            await self.db.commit()
            await self.db.refresh(task)
        return task

    async def delete_task(self, task_id: int):
        task = await self.get_task_by_id(task_id)
        if task:
            await self.db.delete(task)
            await self.db.commit()
        return task 