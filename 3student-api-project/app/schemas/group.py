from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class GroupBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None

class GroupResponse(GroupBase):
    id: int
    created_at: datetime
    updated_at: datetime
    students: List["StudentResponse"] = []  # 改为字符串引用 ✅

    model_config = ConfigDict(from_attributes=True)

class GroupListResponse(BaseModel):
    groups: List[GroupResponse]
    total: int
    page: int
    page_size: int

# 👇 在文件末尾：导入 StudentResponse 并重建模型
from .student import StudentResponse
GroupResponse.model_rebuild()