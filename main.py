from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import students, groups
from app.database.db import engine, Base
import uvicorn
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 关闭时：关闭数据库连接
    await engine.dispose()

app = FastAPI(
    title="Student Management API",
    description="API for managing students and groups",
    version="1.0.0",
    lifespan=lifespan
)

# 包含路由
app.include_router(students.router)
app.include_router(groups.router)

@app.get("/")
async def root():
    return {
        "message": "Student Management API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", 8000)),
        reload=os.getenv("DEBUG", "True").lower() == "true"
    )