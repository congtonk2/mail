# fastapi_user_auth/schemas/auth_schemas.py

from pydantic import BaseModel
from typing import Optional

# 用户注册时的请求数据结构
class UserCreateSchema(BaseModel):
    username: str
    password: str

# 用户登录时的请求数据结构
class UserLoginSchema(BaseModel):
    username: str
    password: str

# 用户信息的返回数据结构
class UserResponseSchema(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True  # 让 Pydantic 支持 SQLAlchemy/SQLModel ORM

# 角色分配的请求数据结构
class RoleAssignSchema(BaseModel):
    user_id: int
    role_key: str

# 用户的详细信息结构，包含角色
class UserDetailResponseSchema(BaseModel):
    id: int
    username: str
    roles: Optional[list] = []
    class Config:
        orm_mode = True

# 角色的返回数据结构
class RoleResponseSchema(BaseModel):
    id: int
    role_key: str
    role_name: str
    class Config:
        orm_mode = True
