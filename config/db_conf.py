from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

# 数据库URL
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/pyfast?charset=utf8mb4"

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    # future=True,
    echo=True,  # 输出sql日志
    pool_size=10,  # 设置连接池中保持的持久连接数
    max_overflow=5,  # 设置连接池允许创建的额外连接数
    pool_timeout=30,  # 超时时间
    pool_pre_ping=True, #取连接时先探活，坏连接自动丢弃重建
    pool_recycle=30, #在 MySQL 超时前主动回收重建（比如小于 wait_timeout）
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)


# 依赖项，用于获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise # 使用raise 将原始异常再次抛出，确保Web框架能捕获到错误
        finally:
            await session.close()
