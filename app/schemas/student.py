from __future__ import annotations
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None

class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    groups: List["GroupResponse"] = []  # 字符串引用 ✅

    model_config = ConfigDict(from_attributes=True)

class StudentListResponse(BaseModel):
    students: List[StudentResponse]
    total: int
    page: int
    page_size: int

# 👇 在文件末尾：导入 GroupResponse 并重建模型
from .group import GroupResponse
StudentResponse.model_rebuild()