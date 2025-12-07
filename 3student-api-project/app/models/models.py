from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base

# 学生-小组关联表（多对多关系）
student_group_association = Table(
    'student_group_association',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id', ondelete="CASCADE")),
    Column('group_id', Integer, ForeignKey('groups.id', ondelete="CASCADE")),
    Column('joined_at', DateTime, default=datetime.utcnow)
)

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    groups = relationship(
        "Group", 
        secondary=student_group_association,
        back_populates="students",
        cascade="all, delete"
    )

class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    students = relationship(
        "Student", 
        secondary=student_group_association,
        back_populates="groups"
    )