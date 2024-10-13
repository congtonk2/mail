# views/operator_views/customer_view.py

from fastapi_amis_admin.admin import ModelAdmin, PageSchema
from models.user import MyUser  # 用户模型
from crud.user_crud import UserCrud
from fastapi_amis_admin.amis.components import ActionType

class CustomerAdmin(ModelAdmin):
    """
    运营专员客户管理视图
    """
    page_schema = PageSchema(label="客户管理", icon="fa fa-user")
    model = MyUser
    search_fields = ["username", "email"]  # 支持根据用户名、邮箱进行搜索
    list_display = ["id", "username", "email", "created_at", "balance", "total_spent"]  # 列表显示字段
    list_filter = ["status"]  # 过滤器：根据客户状态过滤

    def __init__(self, user_crud: UserCrud):
        super().__init__()
        self.user_crud = user_crud

    # 自定义行为，运营专员可以为客户设置分润比例等
    def get_actions(self):
        return [
            {"label": "分配分润比例", "actionType": ActionType.Dialog, "dialog": {"title": "设置分润比例", "body": "设置客户的分润比例"}},
        ]

    # 自定义保存逻辑：创建或更新客户信息
    async def save(self, data):
        return await self.user_crud.create_user(data["username"], data["password"])
