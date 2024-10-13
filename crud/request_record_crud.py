from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.request_record import RequestRecord

class RequestRecordCrud:
    async def create_request_record(self, session: AsyncSession, user_id: int, fission_email: str, project_code: str, amount: float, operator_id: int, revenue_share: float):
        """
        创建请求记录
        """
        request_record = RequestRecord(
            user_id=user_id,
            fission_email=fission_email,
            project_code=project_code,
            amount=amount,
            operator_id=operator_id,
            revenue_share=revenue_share,
            status="pending"
        )
        session.add(request_record)
        await session.commit()
        return request_record

    async def update_request_status(self, session: AsyncSession, request_id: int, status: str):
        """
        更新请求的状态
        """
        request_record = await session.get(RequestRecord, request_id)
        if not request_record:
            raise ValueError("请求记录不存在")

        request_record.status = status
        await session.commit()
        return {"message": f"请求 {request_id} 状态更新为 {status}"}
    
    async def get_user_consumption(self, session: AsyncSession, user_id: int):
        """
        获取用户的消费总额
        """
        statement = select(RequestRecord).where(RequestRecord.user_id == user_id)
        result = await session.execute(statement)
        records = result.scalars().all()
        total_amount = sum(record.amount for record in records)
        return total_amount

    async def get_operator_revenue(self, session: AsyncSession, operator_id: int):
        """
        获取运营专员的分润总额
        """
        statement = select(RequestRecord).where(RequestRecord.operator_id == operator_id)
        result = await session.execute(statement)
        records = result.scalars().all()
        total_revenue = sum(record.amount * record.revenue_share for record in records)
        return total_revenue
