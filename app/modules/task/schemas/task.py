from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# ✅ 子任务 SubTask schema 定义
class SubTask(BaseModel):
    id: int
    title: str
    status: str

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    name: str
    description: str


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    name: Optional[str] = None
    description: Optional[str] = None


class TaskInDBBase(TaskBase):
    id: int
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True


# ✅ 最终返回的 Task 模型，嵌入了 subtask
class Task(TaskInDBBase):
    subtask: Optional[SubTask] = None
