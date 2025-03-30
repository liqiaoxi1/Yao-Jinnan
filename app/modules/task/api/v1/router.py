from fastapi import APIRouter
from app.modules.task.api.v1 import task, daily_report

v1 = APIRouter()
# 每日总结相关接口（建议单独分一个标签）
v1.include_router(daily_report.router, prefix='', tags=['日报功能'])
# 任务相关接口
v1.include_router(task.router, prefix='', tags=['任务管理'])


