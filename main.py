from fastapi import FastAPI
from routers import user
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

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