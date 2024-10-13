from fastapi_user_auth.auth.models import BaseUser
from fastapi_amis_admin.models.fields import Field
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    """定义符合你数据库设计的用户模型"""
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    created_at: Optional[str] = Field(default=None)
    last_login_at: Optional[str] = Field(default=None)
    last_login_ip: Optional[str] = Field(default=None)
    token: Optional[str] = Field(default=None)
    balance: float = Field(default=0)
    status: str = Field(default="active")
    total_spent: float = Field(default=0)
