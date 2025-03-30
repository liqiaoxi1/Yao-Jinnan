from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi import status
from app.modules.user.schemas.user import UserSchema, UserUpdate
from app.modules.user.services.user_service import UserService
from utils.auth import get_auth, Auth
import base64
from typing import Dict

router = APIRouter()

@router.get("/user/info", response_model=UserSchema)
async def get_user_info(auth: Auth = Depends(get_auth)):
    user_service = UserService(auth.db)
    user_id = auth.user_info['sub']
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user = await user_service.get_user_by_id(user_id)
    if user:
        return user
    return {"message": "User not found"}

@router.patch("/user/update", response_model=UserSchema)
async def update_user_properties(update_data: UserUpdate, auth: Auth = Depends(get_auth)):
    user_service = UserService(auth.db)
    user_id = auth.user_info['sub']

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    try:
        updated_user = await user_service.update_user_properties(user_id, update_data)
        if updated_user:
            return updated_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"message": "No update performed"}

@router.post("/user/avatar_update")
async def update_avatar(data: Dict, auth: Auth = Depends(get_auth)):
    try:
        user_id = auth.user_info['sub']
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        try:
            file_data = base64.b64decode(data.get('file'))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid base64 data")

        user_service = UserService(auth.db)
        file_ext = data.get('filename', 'avatar.jpg').split('.')[-1]
        filename = await user_service.update_user_avatar(user_id, file_data, f"avatar.{file_ext}")

        # 更新用户头像URL
        avatar_url = f"/static/avatars/{filename}"
        update_data = UserUpdate(avatar=avatar_url)
        updated_user = await user_service.update_user_properties(user_id, update_data)

        return {
            "code": 200,
            "message": "Avatar updated successfully",
            "data": {
                "url": avatar_url
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/user/name_update", description="修改用户昵称", response_model=UserSchema)
async def name_update(nickname: str, auth: Auth = Depends(get_auth)):
    nickname = nickname.strip()
    if not nickname:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="需要字符")

    user_service = UserService(auth.db)
    user_id = auth.user_info['sub']
    try:
        update_data = UserUpdate(nickname=nickname)
        updated_user = await user_service.update_user_properties(user_id, update_data)
        if updated_user:
            return updated_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "No update performed"}
