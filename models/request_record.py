from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class RequestRecord(SQLModel, table=True):
    """
    用户请求记录表，记录用户的请求、消费金额和分润信息
    """
    request_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", title="用户ID")
    fission_email: str = Field(title="裂变生成的子邮箱")
    project_code: str = Field(title="项目代码")
    amount: float = Field(title="消费金额")
    operator_id: Optional[int] = Field(foreign_key="user.id", title="运营专员ID")  # 运营专员ID
    revenue_share: float = Field(default=0.0, title="分润比例")
    created_at: datetime = Field(default_factory=datetime.utcnow, title="创建时间")
    status: str = Field(default="pending", title="请求状态")
