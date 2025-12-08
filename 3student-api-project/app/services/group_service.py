from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from app.models.models import Group, Student
from app.schemas.group import GroupCreate, GroupUpdate
from typing import List, Optional

class GroupService:
    @staticmethod
    async def create_group(db: AsyncSession, group_data: GroupCreate) -> Group:
        group = Group(**group_data.model_dump())
        db.add(group)
        await db.commit()
        await db.refresh(group)
        return group
    
    @staticmethod
    async def get_group(db: AsyncSession, group_id: int) -> Optional[Group]:
        result = await db.execute(
            select(Group)
            .options(selectinload(Group.students))
            .where(Group.id == group_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_groups(
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Group]:
        result = await db.execute(
            select(Group)
            .options(selectinload(Group.students))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def delete_group(db: AsyncSession, group_id: int) -> bool:
        result = await db.execute(
            delete(Group).where(Group.id == group_id)
        )
        await db.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def get_students_in_group(
        db: AsyncSession, 
        group_id: int
    ) -> List[Student]:
        result = await db.execute(
            select(Group)
            .options(selectinload(Group.students))
            .where(Group.id == group_id)
        )
        group = result.scalar_one_or_none()
        return group.students if group else []