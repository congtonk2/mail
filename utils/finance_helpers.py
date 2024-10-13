# utils/finance_helpers.py

from models.finance import RechargeRecord, FinanceStatistics
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

async def calculate_operator_revenue(session: AsyncSession, operator_id: int) -> float:
    """
    计算运营专员的分润
    :param session: 数据库 session
    :param operator_id: 运营专员ID
    :return: 运营专员的总分润金额
    """
    result = await session.execute(
        "SELECT amount, revenue_share FROM rechargerecord WHERE operator_id = :operator_id AND status = 'completed'",
        {"operator_id": operator_id}
    )
    records = result.fetchall()

    total_revenue = sum(record["amount"] * record["revenue_share"] for record in records)
    return total_revenue

async def record_recharge(session: AsyncSession, user_id: int, amount: float, channel: str) -> RechargeRecord:
    """
    记录用户的充值
    :param session: 数据库 session
    :param user_id: 用户ID
    :param amount: 充值金额
    :param channel: 充值渠道 (如 'gift', 'usdt')
    :return: 充值记录对象
    """
    recharge_record = RechargeRecord(
        user_id=user_id,
        amount=amount,
        channel=channel,
        status="pending"
    )
    session.add(recharge_record)
    await session.commit()
    return recharge_record

async def update_recharge_status(session: AsyncSession, record_id: int, status: str) -> None:
    """
    更新充值记录的状态
    :param session: 数据库 session
    :param record_id: 充值记录ID
    :param status: 更新后的状态 ('pending', 'completed', 'failed')
    """
    await session.execute(
        "UPDATE rechargerecord SET status = :status WHERE id = :record_id",
        {"status": status, "record_id": record_id}
    )
    await session.commit()

async def get_user_finance_statistics(session: AsyncSession, user_id: int) -> FinanceStatistics:
    """
    获取用户的财务统计信息
    :param session: 数据库 session
    :param user_id: 用户ID
    :return: 财务统计对象
    """
    result = await session.execute(
        "SELECT * FROM financestatistics WHERE user_id = :user_id",
        {"user_id": user_id}
    )
    finance_statistics = result.fetchone()
    return finance_statistics
