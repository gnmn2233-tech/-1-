# app/auth.py
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import redis.asyncio as redis
from . import models, schemas
from .config import settings


# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Redis连接池
_redis_pool: Optional[redis.Redis] = None


# ========== 核心修复：安全的密码处理 ==========
def _safe_password_for_bcrypt(password: str) -> str:
    """
    安全处理密码以适应bcrypt的72字节限制
    
    如果密码超过72字节，使用SHA256进行哈希处理
    返回的SHA256哈希值固定为64字节，小于bcrypt限制
    """
    encoded_password = password.encode('utf-8')
    
    # 如果密码长度小于等于72字节，直接返回
    if len(encoded_password) <= 72:
        return password
    
    # 密码过长，使用SHA256哈希
    # SHA256哈希是64个十六进制字符（64字节），小于72字节限制
    return hashlib.sha256(encoded_password).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    safe_password = _safe_password_for_bcrypt(plain_password)
    return pwd_context.verify(safe_password, hashed_password)


def get_password_hash(password: str) -> str:
    """哈希密码"""
    safe_password = _safe_password_for_bcrypt(password)
    return pwd_context.hash(safe_password)
# ========== 修复结束 ==========


def get_redis() -> redis.Redis:
    """获取Redis连接"""
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True
        )
    return _redis_pool


async def close_redis():
    """关闭Redis连接"""
    global _redis_pool
    if _redis_pool:
        await _redis_pool.close()
        _redis_pool = None


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str
) -> Optional[models.User]:
    """通过邮箱和密码验证用户"""
    # 通过邮箱获取用户
    stmt = select(models.User).where(models.User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


def create_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
    token_type: str = "access"
) -> str:
    """创建JWT令牌"""
    to_encode = data.copy()
    
    # 设置过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        if token_type == "access":
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)  # 大写
        else:
            expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)  # 大写
    
    # 编码令牌
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,  # 大写
        algorithm=settings.ALGORITHM  # 大写
    )
    
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[schemas.TokenPayload]:
    """验证JWT令牌"""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        
        # 检查令牌类型
        if payload.get("type") != token_type:
            return None
        
        # 检查过期时间
        if "exp" not in payload:
            return None
        
        # 转换为TokenPayload模式
        token_payload = schemas.TokenPayload(
            sub=payload["sub"],
            jti=payload["jti"],
            type=payload["type"],
            exp=payload["exp"]
        )
        
        return token_payload
    except JWTError:
        return None


async def add_token_to_blacklist(token_payload: schemas.TokenPayload):
    """将令牌添加到Redis黑名单"""
    redis_client = get_redis()
    
    # 计算TTL（距离过期的秒数）
    exp_timestamp = token_payload.exp
    current_timestamp = int(datetime.utcnow().timestamp())
    ttl = max(exp_timestamp - current_timestamp, 60)  # 最少60秒
    
    # 添加令牌到黑名单
    await redis_client.setex(
        f"blacklist:{token_payload.jti}",
        ttl,
        token_payload.type
    )


async def is_token_blacklisted(token_payload: schemas.TokenPayload) -> bool:
    """检查令牌是否在黑名单中"""
    redis_client = get_redis()
    
    # 检查令牌是否在黑名单中
    result = await redis_client.exists(f"blacklist:{token_payload.jti}")
    return result == 1