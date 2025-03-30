from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from utils.auth import get_auth, Auth
from app.modules.task.services.task_service import TaskService
from datetime import datetime
from database.database import get_db

router = APIRouter()

@router.get("/daily_report", summary="生成每日任务总结", description="根据日期生成任务日报")
async def generate_daily_report(
    date: str = Query(..., description="目标日期，格式为 YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
    auth: Auth = Depends(get_auth)
):
    if not auth.user_info.get("sub"):
        raise HTTPException(status_code=401, detail="未经授权")

    try:
        task_service = TaskService(db)
        result = await task_service.generate_daily_report(db, date,auth)
        return {
            "date": date,
            "summary": result
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/daily_report_test")
async def test_report(auth: Auth = Depends(get_auth)):
    return {"message": f"Token OK, 当前用户ID: {auth.user_info.get('sub')}"}

