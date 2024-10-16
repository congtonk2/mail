# admin/__init__.py

# 导出实际需要的 CustomAdminSite
from .site import CustomAdminSite, DocsAdmin, FileAdmin, HomeAdmin, ReDocsAdmin

# 其他需要的导出保留
from .admin import (
    AdminAction,
    AdminApp,
    BaseAdmin,
    BaseAdminSite,
    FormAction,
    FormAdmin,
    IframeAdmin,
    LinkAdmin,
    LinkModelForm,
    ModelAction,
    ModelAdmin,
    PageAdmin,
    PageSchemaAdmin,
    RouterAdmin,
    TemplateAdmin,
)
from .extensions.admin import (
    AutoTimeModelAdmin,
    BaseAuthFieldModelAdmin,
    BaseAuthSelectModelAdmin,
    FootableModelAdmin,
    ReadOnlyModelAdmin,
    SoftDeleteModelAdmin,
)
from .extensions.schemas import (
    FieldPermEnum,
    FilterSelectPerm,
    RecentTimeSelectPerm,
    SelectPerm,
    SimpleSelectPerm,
    UserSelectPerm,
)
from .parser import AmisParser
from .settings import Settings
