# app/schemas.py
from pydantic import BaseModel, EmailStr, Field, UUID4, field_validator
from typing import Optional, List
from datetime import datetime


# ========== 用户相关模式 ==========
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """密码验证（确保不是太长）"""
        if len(v.encode('utf-8')) > 200:  # 设置合理的上限
            raise ValueError('密码过长，请使用较短的密码')
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ========== 令牌相关模式 ==========
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: UUID4  # 用户ID
    jti: str    # 令牌唯一标识符
    type: str   # 令牌类型：access 或 refresh
    exp: int    # 过期时间戳


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ========== 登录历史相关模式 ==========
class LoginHistoryBase(BaseModel):
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None


class LoginHistoryCreate(LoginHistoryBase):
    user_id: UUID4


class LoginHistoryResponse(LoginHistoryBase):
    id: UUID4
    user_id: UUID4
    login_at: datetime
    
    class Config:
        from_attributes = True