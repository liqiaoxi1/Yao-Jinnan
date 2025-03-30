from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
import app.modules.user.services.login_service as login_service
from database.database import get_db
from app.modules.user.services.user_service import UserService
from fastapi.responses import JSONResponse
from core.exceptions import CustomException
from app.modules.user.schemas.user import UserCreate
from utils.auth import get_auth, Auth


router = APIRouter()

@router.post("/register", response_model=UserCreate, responses={200: {"description": "User registered successfully"}, 400: {"description": "Invalid request"}})
async def register_user(user_data: UserCreate, db_session: AsyncSession = Depends(get_db)):
    user_service = UserService(db_session)
    try:
        new_user = await user_service.create_user(user_data)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))