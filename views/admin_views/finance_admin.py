from fastapi_amis_admin.admin import ModelAdmin, PageSchema
from models.finance import RechargeRecord  # 财务模型
from crud.finance_crud import FinanceCrud
from crud.request_record_crud import RequestRecordCrud  # 引入 RequestRecord 的 CRUD
from fastapi_amis_admin.amis.components import ActionType
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


class FinanceAdmin(ModelAdmin):
    """
    管理员财务管理视图
    """
    page_schema = PageSchema(label="财务管理", icon="fa fa-dollar-sign")
    model = RechargeRecord
    search_fields = ["user_id", "channel"]  # 支持根据用户ID或充值渠道搜索
    list_display = ["id", "user_id", "amount", "channel", "status", "created_at"]  # 显示字段
    list_filter = ["status"]  # 过滤器

    def __init__(self, finance_crud: FinanceCrud, request_record_crud: RequestRecordCrud):
        super().__init__()
        self.finance_crud = finance_crud
        self.request_record_crud = request_record_crud  # 初始化 RequestRecord 的 CRUD

    # 自定义行为，如更新充值记录状态
    def get_actions(self):
        return [
            {"label": "标记为完成", "actionType": ActionType.Dialog, "dialog": {"title": "完成充值", "body": "你确定要标记该充值为完成吗？"}},
        ]

    # 自定义保存逻辑，管理充值记录
    async def save(self, data):
        return await self.finance_crud.record_recharge(data["user_id"], data["amount"], data["channel"])

    # 获取用户的消费统计
    async def get_user_consumption(self, session: AsyncSession, user_id: int):
        """
        获取用户的消费统计
        """
        try:
            consumption_data = await self.request_record_crud.get_user_consumption(session, user_id)
            return consumption_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取消费统计失败: {str(e)}")

    # 获取运营专员的分润统计
    async def get_operator_revenue(self, session: AsyncSession, operator_id: int):
        """
        获取运营专员的分润统计
        """
        try:
            revenue_data = await self.request_record_crud.get_operator_revenue(session, operator_id)
            return revenue_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取分润统计失败: {str(e)}")
