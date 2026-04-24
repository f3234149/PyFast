from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from schemas.user import UserRequest
from service import user as user_service
from schemas.user import UserRequest

# router实例
router = APIRouter(prefix="/api/user", tags=["user"])


@router.get("/list")
async def user_list(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    datas = await user_service.user_list(db, skip, limit)
    return {
        "code": 200,
        "message": "success",
        "data": datas
    }


@router.post("/register")
async def register(req: UserRequest,db: AsyncSession = Depends(get_db),):
    exists_user = await user_service.get_user_by_username(db, req.username)
    if exists_user:
        raise HTTPException(status_code=400,detail="用户已存在")
    user = await user_service.create_user(db, req)
    token = await user_service.create_token(db, user.id)
    return {
        "code": 200,
        "message": "success",
        "token": token,
        "data": {
            "username": user.name
        }
    }
