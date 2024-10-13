# models/project.py

from sqlmodel import SQLModel, Field
from typing import Optional

class Project(SQLModel, table=True):
    """项目模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    domain: str = Field(title="项目域名", unique=True, index=True)
    code: str = Field(title="项目代码", unique=True, index=True)
    price_per_use: float = Field(title="单次消费费用")
    max_variants: int = Field(default=5, title="最大裂变次数")
