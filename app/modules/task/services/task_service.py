from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.task.models.task import Task
from app.modules.task.daos.task_dao import TaskDao
from app.modules.task.schemas.task import TaskCreate, TaskUpdate

from app.modules.task.models.task import DailyReport
from sqlalchemy import select



from datetime import datetime, timedelta
from langchain_core.prompts import PromptTemplate
from core.models import llm_GLM




class TaskService:
    def __init__(self, db: AsyncSession):
        self.dao = TaskDao(db)

    async def get_task_by_id(self, task_id: int):
        # 加载一对一的 subtask
        stmt = select(Task).options(selectinload(Task.subtask)).where(Task.id == task_id)
        result = await self.dao.db.execute(stmt)
        return result.scalars().first()

    async def get_all_tasks(self):
        stmt = select(Task).options(selectinload(Task.subtask))
        result = await self.dao.db.execute(stmt)
        return result.scalars().all()

    async def create_task(self, task_data: dict):
        # 检查同名任务是否存在
        existing_task = await self.dao.get_task_by_name(task_data["name"])
        if existing_task:
            raise HTTPException(status_code=400, detail="任务名称已存在")
        return await self.dao.create_task(task_data)

    async def update_task(self, task_id: int, task_data: dict):
        return await self.dao.update_task(task_id, task_data)

    async def delete_task(self, task_id: int):
        return await self.dao.delete_task(task_id)

    async def generate_daily_report(self, db, date: str, auth) -> str:
        """根据指定日期生成当日已完成任务总结（含子任务）"""
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()

            stmt = select(Task).options(selectinload(Task.subtask)).where(
                Task.create_time >= datetime.combine(target_date, datetime.min.time()),
                Task.create_time <= datetime.combine(target_date, datetime.max.time())
            )
            result = await db.execute(stmt)
            tasks = result.scalars().all()

            if not tasks:
                return "当天无已完成的任务"

            prompt = PromptTemplate(
                template=(
                    "请根据以下已完成的任务内容，总结今天的工作成果，帮我拓展我学习内容，及帮我规划明天的学习任务：\n"
                    "{task_summary}\n"
                    "总结应包括主要任务内容、成效或完成情况。"
                ),
                input_variables=["task_summary"]
            )

            summary_parts = []
            for task in tasks:
                task_part = f"任务：{task.name} - {task.description}"
                if task.subtask:
                    task_part += f"，子任务：{task.subtask.title}（状态：{task.subtask.status}）"
                summary_parts.append(task_part)

            all_summary = "；".join(summary_parts)

            chain = prompt | llm_GLM
            response = await chain.ainvoke({
                "task_summary": all_summary
            })
            summary_text = response.content.strip()

            user_id = auth.user_info.get("sub")
            daily_report = DailyReport(
                user_id=user_id,
                date=target_date,
                content=summary_text
            )
            db.add(daily_report)
            await db.commit()

            return summary_text

        except Exception as e:
            raise Exception(f"生成日报失败：{str(e)}")