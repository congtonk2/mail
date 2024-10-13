from fastapi_amis_admin.admin import ModelAdmin, PageSchema
from crud.request_record_crud import RequestRecordCrud  # 使用 RequestRecordCrud
from fastapi_amis_admin.amis.components import ActionType
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


class RevenueAdmin(ModelAdmin):
    """
    运营专员的分润统计视图，基于 RequestRecord 表
    """
    page_schema = PageSchema(label="分润统计", icon="fa fa-chart-line")
    list_display = ["operator_id", "total_revenue"]  # 显示分润数据

    def __init__(self, request_record_crud: RequestRecordCrud):
        super().__init__()
        self.request_record_crud = request_record_crud

    async def get_operator_revenue(self, session: AsyncSession, operator_id: int):
        """
        获取运营专员的分润统计数据
        """
        try:
            revenue_data = await self.request_record_crud.get_operator_revenue(session, operator_id)
            return revenue_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取分润统计失败: {str(e)}")

    # 自定义行为，运营专员可以导出分润报表
    def get_actions(self):
        return [
            {"label": "导出分润报表", "actionType": ActionType.Ajax, "api": "/export_revenue_report"},
        ]

    # 自定义保存逻辑：仅统计分润信息
    async def save(self, data):
        return {"message": "分润统计仅可查看，无法修改"}
