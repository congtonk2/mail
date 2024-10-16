import os.path
import platform
import time
import uuid
from pathlib import Path

import aiofiles
import pydantic
import sqlalchemy
from fastapi import FastAPI, File, UploadFile, Depends
from pydantic import BaseModel
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from models.user import User
from models.admin import Admin

import fastapi_amis_admin
from fastapi_amis_admin import amis
from fastapi_amis_admin.admin import AdminApp, admin
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.amis.components import Page, PageSchema, Property
from fastapi_amis_admin.crud.schema import BaseApiOut
from fastapi_amis_admin.crud.utils import SqlalchemyDatabase
from fastapi_amis_admin.utils.translation import i18n as _

# 导入 fastapi_user_auth 插件
from fastapi_user_auth.admin.site import AuthAdminSite

from fastapi_user_auth.auth import Auth

class APIDocsApp(admin.AdminApp):
    page_schema = PageSchema(label="APIDocs", icon="fa fa-book", sort=-100)

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        if self.app.site.fastapi.docs_url:
            self.register_admin(DocsAdmin)
        if self.app.site.fastapi.redoc_url:
            self.register_admin(ReDocsAdmin)


class DocsAdmin(admin.IframeAdmin):
    page_schema = PageSchema(label="AdminDocs", icon="fa fa-book")

    @property
    def src(self):
        return self.app.site.router_path + self.app.site.fastapi.docs_url


class ReDocsAdmin(admin.IframeAdmin):
    page_schema = PageSchema(label="AdminRedocs", icon="fa fa-book")

    @property
    def src(self):
        return self.app.site.router_path + self.app.site.fastapi.redoc_url


class HomeAdmin(admin.PageAdmin):
    page_schema = PageSchema(label=_("Home"), icon="fa fa-home", url="/home", isDefaultPage=True, sort=100)
    page_path = "/home"

    async def get_page(self, request: Request) -> Page:
        page = await super().get_page(request)
        page.body = [
            Property(
                title="SiteInfo",
                column=4,
                items=[
                    Property.Item(label="title", content=self.site.settings.site_title),
                    Property.Item(label="version", content=self.site.settings.version),
                    Property.Item(label="language", content=self.site.settings.language),
                    Property.Item(label="debug", content=str(self.site.settings.debug)),
                ],
            ),
            amis.Divider(),
            Property(
                title="FastAPI-Amis-Admin",
                column=4,
                items=[
                    Property.Item(label="system", content=platform.system()),
                    Property.Item(label="python", content=platform.python_version()),
                    Property.Item(label="version", content=fastapi_amis_admin.__version__),
                    Property.Item(label="license", content="Apache2.0"),
                    Property.Item(label="amis-cdn", content=self.site.settings.amis_cdn),
                    Property.Item(label="amis-pkg", content=self.site.settings.amis_pkg),
                    Property.Item(label="amis-theme", content=self.site.settings.amis_theme),
                    Property.Item(label="sqlalchemy", content=sqlalchemy.__version__),
                    Property.Item(label="pydantic", content=pydantic.__version__),
                ],
            ),
        ]
        return page


class FileAdmin(admin.RouterAdmin):
    # todo perfect: Limit file size/suffixes/content_type
    file_directory: str = "upload"
    file_path: str = "/upload"
    file_max_size: int = 2 * 1024 * 1024
    router_prefix = "/file"

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.file_directory = self.file_directory or self.file_path
        os.makedirs(self.file_directory, exist_ok=True)
        self.static_path = self.mount_staticfile()

    def get_filename(self, file: UploadFile):
        filename = str(uuid.uuid4()).replace("-", "") + os.path.splitext(file.filename)[1]
        return Path().joinpath(time.strftime("%Y%m"), filename).as_posix()

    def mount_staticfile(self) -> str:
        self.site.fastapi.mount(
            self.file_path,
            StaticFiles(directory=self.file_directory),
            self.file_directory,
        )
        return self.site.router_path + self.file_path

    def register_router(self):
        @self.router.post(self.file_path, response_model=BaseApiOut[self.UploadOutSchema])
        async def file_upload(file: UploadFile = File(...)):
            filename = self.get_filename(file)
            file_path = Path(self.file_directory) / filename
            os.makedirs(file_path.parent, exist_ok=True)
            try:
                res = await file.read()
                if self.file_max_size and len(res) > self.file_max_size:
                    return BaseApiOut(status=-2, msg="The file size exceeds the limit")
                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(res)
                return BaseApiOut(
                    data=self.UploadOutSchema(filename=filename, url=f"{self.static_path}/{filename}"),
                )

            except Exception as e:
                return BaseApiOut(status=-1, msg=str(e))

    class UploadOutSchema(BaseModel):
        filename: str = None
        url: str = None


# 扩展自 AuthAdminSite，用于处理用户认证和权限管理
class CustomAdminSite(AuthAdminSite):
    def __init__(
        self,
        settings: Settings,
        *,
        fastapi: FastAPI = None,
        engine: SqlalchemyDatabase = None,
        auth: Auth = None  # 添加 auth 参数
    ):
        # 调用父类 AuthAdminSite 的初始化，传入设置、FastAPI 实例和数据库引擎
        super().__init__(settings, fastapi=fastapi, engine=engine, auth=auth)
        # 注册需要的管理页面
        self.register_admin(
            HomeAdmin,
            APIDocsApp,
            FileAdmin,
        )

    async def on_startup(self):
        # 调用父类的 on_startup，确保 Casbin 和权限系统正常启动
        await super().on_startup()
        # 创建默认管理员角色和用户
        await self.create_default_users()

    async def create_default_users(self):
        # 如果没有 root 用户，则创建 root 作为超级管理员
        if not await self.auth.get_user_by_username('root'):
            await self.auth.create_role_user(username='root', password='root', role_key='super_admin')

        # 如果没有 admin 用户，则创建 admin 作为普通管理员
        if not await self.auth.get_user_by_username('admin'):
            await self.auth.create_role_user(username='admin', password='admin', role_key='admin')
