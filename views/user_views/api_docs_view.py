# views/user_views/api_docs_view.py

from fastapi_amis_admin.admin import IframeAdmin, PageSchema

class APIDocsView(IframeAdmin):
    """
    普通用户查看 API 文档的视图
    """
    page_schema = PageSchema(label="API 文档", icon="fa fa-book")
    
    @property
    def src(self):
        """
        返回 FastAPI 自动生成的 API 文档的 URL
        """
        return "/docs"  # 指向 FastAPI 默认的 `/docs` 路由

class ReDocsView(IframeAdmin):
    """
    支持 ReDoc 格式的 API 文档视图
    """
    page_schema = PageSchema(label="Redoc API 文档", icon="fa fa-book")

    @property
    def src(self):
        """
        返回 ReDoc 的 API 文档 URL
        """
        return "/redoc"  # 指向 FastAPI 默认的 `/redoc` 路由
