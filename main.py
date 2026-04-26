from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.db_conf import check_db_connection, close_db_engine
from routers import invoice, user


@asynccontextmanager
async def lifespan(_: FastAPI):
    await check_db_connection()
    yield
    await close_db_engine()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 允许的源， 生产环境需要指定源
    allow_credentials=True, # 允许携带cookie
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "fastapi in service..."}


# 挂载路由/注册路由
app.include_router(user.router)
app.include_router(invoice.router)