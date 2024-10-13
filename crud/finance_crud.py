from fastapi_amis_admin.crud import BaseCrud
from models.finance import RechargeRecord, FinanceStatistics
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from utils.functools import logger  # 假设已经设置了一个简单的日志功能

class FinanceCrud(BaseCrud[RechargeRecord]):
    """财务相关的 CRUD 操作"""

    def __init__(self):
        super().__init__(model=RechargeRecord)

    async def record_recharge(self, session: AsyncSession, user_id: int, amount: float, channel: str):
        """
        记录用户充值，添加错误处理和日志记录
        """
        try:
            recharge_record = RechargeRecord(user_id=user_id, amount=amount, channel=channel, status="pending")
            session.add(recharge_record)
            await session.commit()
            logger.info(f"用户 {user_id} 充值记录创建成功，金额: {amount}，渠道: {channel}")
            return recharge_record
        except Exception as e:
            logger.error(f"充值记录创建失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"充值记录创建失败: {str(e)}")

    async def update_recharge_status(self, session: AsyncSession, record_id: int, status: str):
        """
        更新充值记录状态，添加错误处理和日志记录
        """
        try:
            record = await session.get(RechargeRecord, record_id)
            if not record:
                raise ValueError("充值记录不存在")
            record.status = status
            await session.commit()
            logger.info(f"充值记录 {record_id} 状态更新为 {status}")
            return {"message": "充值状态更新成功"}
        except Exception as e:
            logger.error(f"充值状态更新失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"充值状态更新失败: {str(e)}")

    async def get_user_finance_statistics(self, session: AsyncSession, user_id: int):
        """
        获取用户的财务统计信息，添加错误处理
        """
        try:
            statement = select(FinanceStatistics).where(FinanceStatistics.user_id == user_id)
            result = await session.execute(statement)
            finance_data = result.scalars().first()
            if not finance_data:
                raise ValueError("未找到用户的财务统计信息")
            return finance_data
        except Exception as e:
            logger.error(f"获取用户 {user_id} 财务统计信息失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"获取用户财务统计信息失败: {str(e)}")

    async def calculate_operator_revenue(self, session: AsyncSession, operator_id: int):
        """
        计算运营专员的分润，添加错误处理和边界条件处理，确保无记录时返回 0
        """
        try:
            statement = select(RechargeRecord).where(RechargeRecord.operator_id == operator_id)
            result = await session.execute(statement)
            records = result.scalars().all()

            # 处理无记录的情况，返回 0
            if not records:
                logger.info(f"运营专员 {operator_id} 无消费记录，分润为 0")
                return {"operator_id": operator_id, "total_revenue": 0.0}

            total_revenue = sum(record.amount * record.revenue_share for record in records)
            logger.info(f"运营专员 {operator_id} 总分润: {total_revenue}")
            return {"operator_id": operator_id, "total_revenue": total_revenue}
        except Exception as e:
            logger.error(f"分润计算失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"分润计算失败: {str(e)}")
