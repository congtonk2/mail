# fastapi_user_auth/models/user.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    """用户模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, title="用户名")
    password_hash: str = Field(title="密码哈希")
    roles: List["Role"] = Relationship(back_populates="users")  # 多对多关系

class Role(SQLModel, table=True):
    """角色模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    role_key: str = Field(unique=True, title="角色标识符", description="如 'admin', 'operator'")
    role_name: str = Field(title="角色名称", description="显示给用户的角色名称")
    users: List["User"] = Relationship(back_populates="roles")  # 多对多关系
