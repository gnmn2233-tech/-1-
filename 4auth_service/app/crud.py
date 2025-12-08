# app/crud.py
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from . import models, schemas
from .auth import get_password_hash


async def get_user(db: AsyncSession, user_id: UUID) -> Optional[models.User]:
    """通过ID获取用户"""
    stmt = select(models.User).where(models.User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[models.User]:
    """通过邮箱获取用户"""
    stmt = select(models.User).where(models.User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    user_data: schemas.UserCreate
) -> models.User:
    """创建新用户"""
    # 哈希密码
    hashed_password = get_password_hash(user_data.password)
    
    # 创建用户
    db_user = models.User(
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    await db.flush()
    
    return db_user


async def update_user(
    db: AsyncSession,
    user: models.User,
    user_data: schemas.UserUpdate
) -> models.User:
    """更新用户数据"""
    update_data = user_data.model_dump(exclude_unset=True)
    
    # 如果提供了邮箱，更新邮箱
    if "email" in update_data and update_data["email"]:
        user.email = update_data["email"]
    
    # 如果提供了密码，更新密码
    if "password" in update_data and update_data["password"]:
        user.hashed_password = get_password_hash(update_data["password"])
    
    await db.flush()
    return user


async def create_login_history(
    db: AsyncSession,
    login_data: schemas.LoginHistoryCreate
) -> models.LoginHistory:
    """创建登录历史记录"""
    db_login = models.LoginHistory(
        user_id=login_data.user_id,
        user_agent=login_data.user_agent,
        ip_address=login_data.ip_address
    )
    
    db.add(db_login)
    await db.flush()
    
    return db_login


async def get_user_login_history(
    db: AsyncSession,
    user_id: UUID,
    skip: int = 0,
    limit: int = 100
) -> List[models.LoginHistory]:
    """获取用户登录历史（带分页）"""
    stmt = (
        select(models.LoginHistory)
        .where(models.LoginHistory.user_id == user_id)
        .order_by(desc(models.LoginHistory.login_at))
        .offset(skip)
        .limit(limit)
    )
    
    result = await db.execute(stmt)
    return result.scalars().all()