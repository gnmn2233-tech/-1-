from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from app.models.models import Student, Group
from app.schemas.student import StudentCreate, StudentUpdate
from typing import List, Optional

class StudentService:
    @staticmethod
    async def create_student(db: AsyncSession, student_data: StudentCreate) -> Student:
        student = Student(**student_data.model_dump())
        db.add(student)
        await db.commit()
        await db.refresh(student)
        return student
    
    @staticmethod
    async def get_student(db: AsyncSession, student_id: int) -> Optional[Student]:
        result = await db.execute(
            select(Student)
            .options(selectinload(Student.groups))
            .where(Student.id == student_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_students(
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Student]:
        result = await db.execute(
            select(Student)
            .options(selectinload(Student.groups))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def delete_student(db: AsyncSession, student_id: int) -> bool:
        result = await db.execute(
            delete(Student).where(Student.id == student_id)
        )
        await db.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def add_student_to_group(
        db: AsyncSession, 
        student_id: int, 
        group_id: int
    ) -> bool:
        # 获取学生和小组
        student_result = await db.execute(
            select(Student).where(Student.id == student_id)
        )
        group_result = await db.execute(
            select(Group).where(Group.id == group_id)
        )
        
        student = student_result.scalar_one_or_none()
        group = group_result.scalar_one_or_none()
        
        if student and group:
            # 检查是否已经在小组中
            if group not in student.groups:
                student.groups.append(group)
                await db.commit()
                return True
        return False
    
    @staticmethod
    async def remove_student_from_group(
        db: AsyncSession, 
        student_id: int, 
        group_id: int
    ) -> bool:
        student_result = await db.execute(
            select(Student).where(Student.id == student_id)
        )
        group_result = await db.execute(
            select(Group).where(Group.id == group_id)
        )
        
        student = student_result.scalar_one_or_none()
        group = group_result.scalar_one_or_none()
        
        if student and group and group in student.groups:
            student.groups.remove(group)
            await db.commit()
            return True
        return False
    
    @staticmethod
    async def transfer_student(
        db: AsyncSession, 
        student_id: int, 
        from_group_id: int, 
        to_group_id: int
    ) -> bool:
        # 先移除原小组，再加入新小组
        removed = await StudentService.remove_student_from_group(
            db, student_id, from_group_id
        )
        if removed:
            added = await StudentService.add_student_to_group(
                db, student_id, to_group_id
            )
            return added
        return False