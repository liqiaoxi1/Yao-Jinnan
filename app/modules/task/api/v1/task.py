from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.modules.task.schemas.task import Task, TaskCreate, TaskUpdate
from app.modules.task.services.task_service import TaskService
from utils.auth import get_auth, Auth

router = APIRouter()

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED, summary="创建任务")
async def create_task(
    task_in: TaskCreate,
    auth: Auth = Depends(get_auth)
) -> Task:
    """
    创建新任务
    """
    if not auth.user_info.get('sub'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未经授权"
        )
    
    try:
        task_service = TaskService(auth.db)
        return await task_service.create_task(task_in.dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"创建任务失败: {str(e)}"
        )

@router.put("/{task_id}", response_model=Task, summary="更新任务")
async def update_task(
    task_id: int,
    task_in: TaskUpdate,
    auth: Auth = Depends(get_auth)
) -> Task:
    """
    更新任务信息
    """
    if not auth.user_info.get('sub'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未经授权"
        )
    
    try:
        task_service = TaskService(auth.db)
        task = await task_service.update_task(task_id, task_in.dict(exclude_unset=True))
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到该任务"
            )
        return task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"更新任务失败: {str(e)}"
        )

@router.get("/{task_id}", response_model=Task, summary="获取任务详情")
async def get_task(
    task_id: int,
    auth: Auth = Depends(get_auth)
) -> Task:
    """
    获取指定任务的详细信息
    """
    if not auth.user_info.get('sub'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未经授权"
        )
    
    task_service = TaskService(auth.db)
    task = await task_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到该任务"
        )
    return task

@router.get("/", response_model=List[Task], summary="获取任务列表")
async def get_tasks(
    auth: Auth = Depends(get_auth)
) -> List[Task]:
    """
    获取所有任务列表
    """
    if not auth.user_info.get('sub'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未经授权"
        )
    
    task_service = TaskService(auth.db)
    tasks = await task_service.get_all_tasks()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到任何任务"
        )
    return tasks

@router.delete("/{task_id}", response_model=Task, summary="删除任务")
async def delete_task(
    task_id: int,
    auth: Auth = Depends(get_auth)
) -> Task:
    """
    删除指定任务
    """
    if not auth.user_info.get('sub'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未经授权"
        )
    
    try:
        task_service = TaskService(auth.db)
        task = await task_service.delete_task(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到该任务"
            )
        return task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"删除任务失败: {str(e)}"
        ) 



