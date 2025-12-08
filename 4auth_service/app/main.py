# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
from sqlalchemy import text
from app import auth
from app.config import settings
from app.database import engine
from app.routers import auth as auth_router
from app.routers import users as users_router

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动
    logger.info("启动Auth服务...")
    
    # 测试数据库连接（修复：使用正确的异步API）
    logger.info("测试数据库连接...")
    try:
        async with engine.connect() as conn:
            # 修复：使用text()包装SQL语句
            await conn.execute(text("SELECT 1"))
            await conn.commit()
            logger.info("数据库连接成功")
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        # 不抛出异常，让应用继续启动
    
    # 测试Redis连接
    logger.info("测试Redis连接...")
    try:
        redis_client = auth.get_redis()
        await redis_client.ping()
        logger.info("Redis连接成功")
    except Exception as e:
        logger.warning(f"Redis连接警告: {e}（继续运行）")
    
    logger.info("Auth服务启动完成")
    
    yield
    
    # 关闭
    logger.info("关闭服务...")
    await auth.close_redis()


# 创建FastAPI应用
app = FastAPI(
    title="Auth Service API",
    description="使用JWT令牌的认证和授权服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # 与allow_origins=["*"]兼容
    allow_methods=["*"],
    allow_headers=["*"],
)


# 异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "内部服务器错误"},
    )


# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 测试数据库
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    try:
        # 测试Redis
        redis_client = auth.get_redis()
        redis_ping = await redis_client.ping()
        redis_status = "healthy" if redis_ping else "unhealthy"
    except Exception as e:
        redis_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy",
        "service": "auth-service",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "database": db_status,
            "redis": redis_status
        }
    }


# 包含路由
app.include_router(auth_router.router)
app.include_router(users_router.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )