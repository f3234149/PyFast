from fastapi import FastAPI
from routers import user
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 挂载路由/注册路由
app.include_router(user.router)