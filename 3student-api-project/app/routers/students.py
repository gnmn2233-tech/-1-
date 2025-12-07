from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.db import get_db
from app.schemas.student import (
    StudentCreate, 
    StudentResponse, 
    StudentUpdate,
    StudentListResponse
)
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    student: StudentCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建学生"""
    return await StudentService.create_student(db, student)

@router.get("/", response_model=StudentListResponse)
async def get_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: AsyncSession = Depends(get_db)
):
    """获取学生列表"""
    students = await StudentService.get_students(db, skip, limit)
    total = len(students)
    return StudentListResponse(
        students=students,
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        page_size=limit
    )

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    """根据ID获取学生信息"""
    student = await StudentService.get_student(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    """删除学生"""
    deleted = await StudentService.delete_student(db, student_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

@router.post("/{student_id}/groups/{group_id}", status_code=status.HTTP_200_OK)
async def add_student_to_group(
    student_id: int,
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    """添加学生到小组"""
    success = await StudentService.add_student_to_group(db, student_id, group_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student or Group not found"
        )
    return {"message": "Student added to group successfully"}

@router.delete("/{student_id}/groups/{group_id}", status_code=status.HTTP_200_OK)
async def remove_student_from_group(
    student_id: int,
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    """从小组中移除学生"""
    success = await StudentService.remove_student_from_group(db, student_id, group_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student or Group not found, or student not in group"
        )
    return {"message": "Student removed from group successfully"}

@router.put("/{student_id}/transfer", status_code=status.HTTP_200_OK)
async def transfer_student(
    student_id: int,
    from_group_id: int = Query(..., description="原小组ID"),
    to_group_id: int = Query(..., description="目标小组ID"),
    db: AsyncSession = Depends(get_db)
):
    """将学生从一个小组转移到另一个小组"""
    success = await StudentService.transfer_student(
        db, student_id, from_group_id, to_group_id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transfer failed. Check student and group IDs"
        )
    return {"message": "Student transferred successfully"}