from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from service import user as user_service

# router实例
router = APIRouter(prefix="/api/user", tags=["user"])


@router.get("/list")
async def user_list(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    datas = await user_service.user_list(db, skip, limit)
    return {
        "code": 200,
        "message": "success",
        "data":datas
    }
