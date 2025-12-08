# app/routers/users.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud, dependencies
from app.database import get_db


router = APIRouter(prefix="/user", tags=["users"])


@router.put("/update", response_model=schemas.UserResponse)
async def update_user(
    user_data: schemas.UserUpdate,
    current_user: schemas.UserResponse = Depends(dependencies.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户数据"""
    # 从数据库获取用户
    user = await crud.get_user(db, current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 检查新邮箱是否已存在
    if user_data.email and user_data.email != current_user.email:
        existing_user = await crud.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="该邮箱已被注册"
            )
    
    # 更新用户
    updated_user = await crud.update_user(db, user, user_data)
    
    return schemas.UserResponse.model_validate(updated_user)


@router.get("/history", response_model=List[schemas.LoginHistoryResponse])
async def get_login_history(
    current_user: schemas.UserResponse = Depends(dependencies.get_current_user),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """获取用户登录历史"""
    # 获取登录历史
    history = await crud.get_user_login_history(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    
    return [schemas.LoginHistoryResponse.model_validate(item) for item in history]