# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud, auth, dependencies
from app.database import get_db


router = APIRouter(prefix="", tags=["authentication"])
security = HTTPBearer()


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """注册新用户"""
    # 检查用户是否已存在
    existing_user = await crud.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="该邮箱已被注册"
        )
    
    # 创建新用户
    user = await crud.create_user(db, user_data)
    
    return schemas.UserResponse.model_validate(user)


@router.post("/login", response_model=schemas.Token)
async def login(
    request: Request,
    login_data: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """用户登录并返回令牌"""
    # 验证用户
    user = await auth.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误"
        )
    
    # 从请求中获取用户代理和IP
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None
    
    # 创建登录历史记录
    await crud.create_login_history(
        db,
        schemas.LoginHistoryCreate(
            user_id=user.id,
            user_agent=user_agent,
            ip_address=ip_address
        )
    )
    
    # 创建令牌
    access_token = auth.create_token(
        data={"sub": str(user.id)},
        token_type="access"
    )
    
    refresh_token = auth.create_token(
        data={"sub": str(user.id)},
        token_type="refresh"
    )
    
    return schemas.Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(
    token_payload: schemas.TokenPayload = Depends(dependencies.get_refresh_token_payload),
    db: AsyncSession = Depends(get_db)
):
    """使用刷新令牌刷新访问令牌"""
    # 检查用户是否存在
    user = await crud.get_user(db, user_id=token_payload.sub)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    
    # 将旧的刷新令牌加入黑名单
    await auth.add_token_to_blacklist(token_payload)
    
    # 创建新令牌
    access_token = auth.create_token(
        data={"sub": str(user.id)},
        token_type="access"
    )
    
    refresh_token = auth.create_token(
        data={"sub": str(user.id)},
        token_type="refresh"
    )
    
    return schemas.Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/logout")
async def logout(
    current_user: schemas.UserResponse = Depends(dependencies.get_current_user),
    credentials: str = Depends(security)
):
    """用户退出登录"""
    token = credentials.credentials
    
    # 验证令牌
    token_payload = auth.verify_token(token, token_type="access")
    if token_payload:
        # 将令牌加入黑名单
        await auth.add_token_to_blacklist(token_payload)
    
    return {"message": "成功退出登录"}