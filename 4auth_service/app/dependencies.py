# app/dependencies.py
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas, crud, auth
from .database import get_db


security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> schemas.UserResponse:
    """依赖项：获取当前认证用户"""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未认证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    # 验证令牌
    token_payload = auth.verify_token(token, token_type="access")
    if token_payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效或过期的令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查令牌是否在黑名单中
    if await auth.is_token_blacklisted(token_payload):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌已被撤销",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 从数据库获取用户
    user = await crud.get_user(db, user_id=token_payload.sub)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 在请求状态中存储用户ID（用于日志记录）
    request.state.user_id = str(user.id)
    
    return schemas.UserResponse.model_validate(user)


async def get_refresh_token_payload(
    refresh_token_request: schemas.RefreshTokenRequest
) -> schemas.TokenPayload:
    """从刷新令牌获取payload"""
    token_payload = auth.verify_token(
        refresh_token_request.refresh_token,
        token_type="refresh"
    )
    
    if token_payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效或过期的刷新令牌"
        )
    
    # 检查刷新令牌是否在黑名单中
    if await auth.is_token_blacklisted(token_payload):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="刷新令牌已被撤销"
        )
    
    return token_payload