import logging
from typing import Any, Union
from typing_extensions import Literal
from fastapi_amis_admin.amis import API
from fastapi_amis_admin.utils.pydantic import PYDANTIC_V2, BaseSettings


class Settings(BaseSettings):
    """项目配置类"""

    host: str = "127.0.0.1"  # 服务器主机地址
    port: int = 8000  # 服务器端口
    debug: bool = False  # 调试模式
    version: str = "0.0.0"  # 项目版本
    site_title: str = "我的后台管理系统"  # 站点标题（可自定义）
    site_icon: str = "https://baidu.github.io/amis/static/logo_408c434.png"  # 站点图标
    site_url: str = ""  # 站点URL
    site_path: str = "/admin"  # 后台管理路径
    database_url_async: str = ""  # 异步数据库连接URL
    database_url: str = ""  # 数据库连接URL
    language: Union[Literal["zh_CN", "en_US", "de_DE"], str] = "zh_CN"  # 语言设置（默认为中文）
    amis_cdn: str = "https://unpkg.com"  # AMIS 前端框架的 CDN 地址
    amis_pkg: str = "amis@6.3.0"  # AMIS 前端框架的版本
    amis_theme: Literal["cxd", "antd", "dark", "ang"] = "cxd"  # AMIS 主题（可选择 cxd, antd, dark, ang）
    amis_image_receiver: API = None  # 图片上传接口
    amis_file_receiver: API = None  # 文件上传接口
    logger: Union[logging.Logger, Any] = logging.getLogger("fastapi_amis_admin")  # 日志配置

    @classmethod
    def valid_url_(cls, url: str):
        # 确保 URL 结尾不带斜杠
        return url[:-1] if url.endswith("/") else url

    @classmethod
    def valid_database_url_(cls, values):
        # 设置默认的文件上传接口
        file_upload_api = f"post:{values.get('site_path', '')}/file/upload"
        values.setdefault("amis_image_receiver", file_upload_api)
        values.setdefault("amis_file_receiver", file_upload_api)

        # 设置默认的数据库 URL
        if not values.get("database_url") and not values.get("database_url_async"):
            values.setdefault(
                "database_url_async",
                "sqlite+aiosqlite:///amisadmin.db?check_same_thread=False",
            )
        return values

    if PYDANTIC_V2:
        from pydantic import field_validator, model_validator

        valid_url = field_validator("amis_cdn", "site_path", "site_url", mode="before")(lambda cls, v: cls.valid_url_(v))
        valid_database_url = model_validator(mode="before")(lambda cls, values: cls.valid_database_url_(values))

    else:
        from pydantic import root_validator, validator

        valid_url = validator("amis_cdn", "site_path", "site_url", pre=True)(lambda cls, v: cls.valid_url_(v))
        valid_database_url = root_validator(pre=True, allow_reuse=True)(lambda cls, values: cls.valid_database_url_(values))


if PYDANTIC_V2:
    Settings.model_rebuild()  # 如果使用了 Pydantic v2，重建模型
