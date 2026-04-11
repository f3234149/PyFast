from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User

async def user_list(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()