import uuid
from datetime import datetime, timedelta
from idlelib import query

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User, UserToken
from schemas.user import UserRequest
from utils import security


async def user_list(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.name == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserRequest):
    password_hash = security.get_password_hash(user_data.password)
    user = User(name=user_data.username, password=password_hash)
    db.add(user)
    await db.commit()
    await db.refresh(user)  # 返回最新的user
    return user


async def create_token(db: AsyncSession, user_id: int):
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=2)
    token_query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(token_query)
    user_token_result = result.scalar_one_or_none()
    if user_token_result:
        user_token_result.token = token
        user_token_result.expires_at = expires_at
    else:
        token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(token)
        await db.commit()
    return token
