# fastapi_user_auth/auth/auth.py

from fastapi import Depends, HTTPException
from fastapi_user_auth.auth import Auth
from fastapi_user_auth.auth.models import User
from fastapi import Request

# 创建 Auth 实例
auth = Auth()

async def get_current_user(request: Request) -> User:
    """
    获取当前登录的用户
    """
    user = await auth.get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="认证失败，用户未登录")
    return user

# 验证用户是否拥有指定角色
async def require_role(request: Request, roles: list = None):
    """
    验证用户是否拥有指定的角色
    """
    user = await get_current_user(request)
    if not roles or not auth.enforcer.has_any_role(user, roles):
        raise HTTPException(status_code=403, detail="无权限访问")
    return user

# 用户注册
async def register_user(username: str, password: str):
    """
    注册新用户
    """
    if await auth.get_user_by_username(username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = await auth.create_role_user(username=username, password=password)
    return user

# 用户登录
async def login_user(request: Request, username: str, password: str):
    """
    用户登录逻辑
    """
    user = await auth.authenticate_user(username=username, password=password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 返回 token 或其他认证信息
    return {"token": await auth.create_access_token(user)}
