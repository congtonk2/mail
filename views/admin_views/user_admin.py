# views/admin_views/user_admin.py

from fastapi_amis_admin.admin import ModelAdmin, PageSchema
from fastapi_user_auth.auth.models import MyUser
from crud.user_crud import UserCrud
from fastapi_amis_admin.amis.components import ActionType

class UserAdmin(ModelAdmin):
    """
    管理员用户管理视图
    """
    page_schema = PageSchema(label="用户管理", icon="fa fa-users")
    model = MyUser
    search_fields = ["username"]  # 支持根据用户名搜索
    list_display = ["id", "username", "created_at"]  # 列表显示的字段
    list_filter = ["status"]  # 过滤器

    def __init__(self, user_crud: UserCrud):
        super().__init__()
        self.user_crud = user_crud

    # 自定义行为，可以添加按钮如：封禁用户、解封用户等
    def get_actions(self):
        return [
            {"label": "封禁用户", "actionType": ActionType.Dialog, "dialog": {"title": "封禁用户", "body": "你确定要封禁该用户吗？"}},
            {"label": "解封用户", "actionType": ActionType.Dialog, "dialog": {"title": "解封用户", "body": "你确定要解封该用户吗？"}},
        ]

    # 自定义保存逻辑
    async def save(self, data):
        return await self.user_crud.create_user(data["username"], data["password"])
