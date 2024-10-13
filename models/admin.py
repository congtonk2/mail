from sqlmodel import SQLModel, Field
from typing import Optional

class Admin(SQLModel, table=True):
    """定义管理员模型，符合数据库设计"""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    created_at: Optional[str] = Field(default=None)
    last_login_at: Optional[str] = Field(default=None)
    last_login_ip: Optional[str] = Field(default=None)
    role: str = Field(default="admin")  # super_admin, admin, operator
    permissions: Optional[str] = Field(default=None)  # JSON 字段
