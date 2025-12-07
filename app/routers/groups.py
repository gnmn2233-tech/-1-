from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.db import get_db
from app.schemas.group import (
    GroupCreate, 
    GroupResponse, 
    GroupUpdate,
    GroupListResponse
)
from app.schemas.student import StudentResponse
from app.services.group_service import GroupService

router = APIRouter(prefix="/groups", tags=["groups"])

@router.post("/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    group: GroupCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建小组"""
    return await GroupService.create_group(db, group)

@router.get("/", response_model=GroupListResponse)
async def get_groups(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: AsyncSession = Depends(get_db)
):
    """获取小组列表"""
    groups = await GroupService.get_groups(db, skip, limit)
    total = len(groups)
    return GroupListResponse(
        groups=groups,
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        page_size=limit
    )

@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    """根据ID获取小组信息"""
    group = await GroupService.get_group(db, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    return group

@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    """删除小组"""
    deleted = await GroupService.delete_group(db, group_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )

@router.get("/{group_id}/students", response_model=List[StudentResponse])
async def get_students_in_group(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取小组内的所有学生"""
    students = await GroupService.get_students_in_group(db, group_id)
    if not students:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found or no students in group"
        )
    return students