# views/user_views/profile_view.py

from fastapi_amis_admin.admin import PageAdmin, PageSchema
from fastapi_amis_admin.amis.components import Form, InputText, ActionType, Html, Button

class ProfileView(PageAdmin):
    """
    普通用户的个人中心视图
    """
    page_schema = PageSchema(label="个人中心", icon="fa fa-user")
    page_path = "/profile"

    async def get_page(self, request):
        user = request.user  # 当前登录的用户

        # 个人信息展示
        return Form(
            title="个人信息",
            body=[
                InputText(name="username", label="用户名", value=user.username, disabled=True),
                InputText(name="balance", label="余额", value=user.balance, disabled=True),
                InputText(name="token", label="Token", value=user.token, disabled=True),
                Html("<br>"),
                Button(label="更新Token", actionType=ActionType.Ajax, api="/user/update_token"),
                Button(label="修改密码", actionType=ActionType.Dialog, dialog={"title": "修改密码", "body": "请输入新密码"}),
            ]
        )
