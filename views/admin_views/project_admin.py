# views/admin_views/project_admin.py

from fastapi_amis_admin.admin import ModelAdmin, PageSchema
from models.project import Project  # 假设有 Project 模型
from fastapi_amis_admin.amis.components import ActionType
from crud.project_crud import ProjectCrud  # 项目的 CRUD 操作
from fastapi import HTTPException


class ProjectAdmin(ModelAdmin):
    """
    管理员项目管理视图
    """
    page_schema = PageSchema(label="项目管理", icon="fa fa-briefcase")
    model = Project
    search_fields = ["domain", "code"]  # 支持根据域名或项目代码搜索
    list_display = ["id", "domain", "code", "price_per_use", "max_variants"]  # 列表显示的字段

    def __init__(self, project_crud: ProjectCrud):
        super().__init__()
        self.project_crud = project_crud

    # 自定义行为，如调整项目的单价
    def get_actions(self):
        return [
            {"label": "编辑项目", "actionType": ActionType.Dialog, "dialog": {"title": "编辑项目", "body": "请更新项目信息"}},
        ]

    # 自定义保存逻辑
    async def save(self, data):
        return await self.project_crud.create_project(data)
