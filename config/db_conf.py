"""
Database engine and session factory.

All connection parameters come from config/settings.yaml via app_conf.
Active database is selected by APP_DB in .env.
"""
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config.app_conf import get_db_config

_cfg = get_db_config()

async_engine = create_async_engine(
    _cfg.async_url,
    echo=_cfg.echo,
    pool_size=_cfg.pool_size,
    max_overflow=_cfg.max_overflow,
    pool_timeout=_cfg.pool_timeout,
    pool_pre_ping=True,
    pool_recycle=_cfg.pool_recycle,
    connect_args={
        "connect_timeout": _cfg.connect_timeout,
        # "read_timeout": _cfg.read_timeout,
        # "write_timeout": _cfg.write_timeout,
    },
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def check_db_connection() -> None:
    async with async_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))


async def close_db_engine() -> None:
    await async_engine.dispose()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
