from fastapi import APIRouter
from app.modules.user.api.router import v1 as user_router
from app.modules.task.api.router import v1 as task_router

route = APIRouter(prefix='/api/v1')  # 接口版本v1

route.include_router(user_router)
route.include_router(task_router)

