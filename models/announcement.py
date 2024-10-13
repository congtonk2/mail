# models/announcement.py

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Announcement(SQLModel, table=True):
    """公告模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(title="公告标题")
    content: str = Field(title="公告内容")
    created_at: datetime = Field(default_factory=datetime.utcnow, title="创建时间")
