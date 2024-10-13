# models/finance.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from models.user import User  # 导入自定义的用户模型

class RechargeRecord(SQLModel, table=True):
    """充值记录模型"""
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="auth_user.id", title="用户ID")
    amount: float = Field(title="充值金额")
    channel: str = Field(title="充值渠道")  # 例如 'gift'、'usdt' 等
    order_id: Optional[str] = Field(None, title="订单ID")
    created_at: datetime = Field(default_factory=datetime.utcnow, title="充值时间")
    status: str = Field(default="pending", title="充值状态")  # 'pending'、'completed'、'failed'
    balance_after: Optional[float] = Field(None, title="充值后的余额")
    # 用户与充值记录的关系
    user: Optional["User"] = Relationship(back_populates="recharge_records")  # 使用 User 代替 MyUser

class FinanceStatistics(SQLModel, table=True):
    """财务统计模型"""
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="auth_user.id", title="用户ID")
    total_recharge: float = Field(default=0.0, title="总充值金额")
    total_spent: float = Field(default=0.0, title="总消费金额")
    operator_revenue: float = Field(default=0.0, title="运营员分润总额")
    created_at: datetime = Field(default_factory=datetime.utcnow, title="统计时间")
    # 关联到用户
    user: Optional["User"] = Relationship()  # 使用 User 代替 MyUser

