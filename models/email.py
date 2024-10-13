# models/email.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class EmailResource(SQLModel, table=True):
    """父邮箱模型，存储父邮箱及其 SMTP 配置信息"""
    email_id: int = Field(default=None, primary_key=True)
    parent_email: str = Field(title="父邮箱地址")
    parent_password: str = Field(title="父邮箱密码")
    smtp_email: str = Field(title="SMTP邮箱地址")
    smtp_password: str = Field(title="SMTP邮箱密码")
    status: str = Field(default="available", title="邮箱状态")  # 'available'、'disabled'、'banned'
    created_at: datetime = Field(default_factory=datetime.utcnow, title="创建时间")
    # 记录剩余裂变次数，每个项目的剩余裂变数通过 JSON 存储
    variants_left: dict = Field(default={}, title="剩余裂变次数", description="每个项目的剩余裂变次数")
    # 父邮箱与子邮箱的关系
    child_emails: List["ChildEmail"] = Relationship(back_populates="parent_email")

class ChildEmail(SQLModel, table=True):
    """子邮箱模型，由父邮箱裂变生成的子邮箱"""
    child_email_id: int = Field(default=None, primary_key=True)
    parent_email_id: int = Field(foreign_key="emailresource.email_id", title="父邮箱ID")
    generated_email: str = Field(title="生成的子邮箱地址")
    project_code: str = Field(title="项目代码", description="分配给哪个项目")
    status: str = Field(default="unused", title="子邮箱状态")  # 'unused'、'used'、'waiting'、'timeout'
    created_at: datetime = Field(default_factory=datetime.utcnow, title="生成时间")
    completed_projects: dict = Field(default={}, title="完成的项目", description="子邮箱完成的项目记录")
    # 子邮箱与父邮箱的关系
    parent_email: Optional["EmailResource"] = Relationship(back_populates="child_emails")

