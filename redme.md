fastapi_admin_project/
    ├── main.py                       # 主应用入口，配置 FastAPI 和 fastapi-amis-admin
    ├── config.py                     # 配置文件，包含数据库 URL 等设定
    ├── database.py                   # 数据库连接设置
    ├── initialize_db.py              # 数据库初始化脚本

    ├── fastapi_amis_admin/           # 管理后台功能，集成 GitHub 的 fastapi-amis-admin
    │   ├── admin/                    # 管理后台页面配置
    │   │   ├── handlers.py           # 管理后台的请求处理器
    │   │   ├── parser.py             # 用于 Amis 页面解析的工具
    │   │   ├── settings.py           # 管理后台设置配置
    │   │   ├── site.py               # 管理后台站点配置
    │   │   └── extensions/           # 管理后台扩展功能
    │   │       ├── admin.py          # 扩展的模型管理功能（如只读、软删除等）
    │   │       ├── schemas.py        # 权限控制相关数据结构
    │   │       └── utils.py          # 辅助函数
    │   ├── amis/                     # Amis 前端页面配置
    │   │   ├── types.py              # 定义 Amis 组件的基础类型
    │   │   ├── components.py         # 定义前端页面的各种组件
    │   │   ├── constants.py          # 定义组件常量，如按钮样式等
    │   │   ├── utils.py              # 包含模板辅助函数
    │   │   └── __init__.py           # 初始化 Amis 模块
    │   ├── crud/                     # 增删改查操作逻辑，包含自定义和自动生成 CRUD
    │   │   ├── _sqlalchemy.py        # SQLAlchemy 相关的 CRUD 操作工具
    │   │   ├── _sqlmodel.py          # SqlModel 相关的 CRUD 工具
    │   │   ├── base.py               # 基础 CRUD 管理类
    │   │   ├── parser.py             # CRUD 操作的解析工具
    │   │   ├── schema.py             # 数据模型的 CRUD Schema
    │   │   └── utils.py              # CRUD 相关的工具函数
    │   ├── globals/                  # 全局变量和配置
    │   │   ├── _db.py                # 数据库连接全局管理工具
    │   │   ├── _sites.py             # 站点全局管理工具
    │   │   ├── core.py               # 全局变量管理工具
    │   │   └── deps.py               # FastAPI 的依赖管理
    │   ├── models/                   # 数据库模型，包含业务模型
    │   │   ├── fields.py             # 自定义的 SQLAlchemy 字段类型
    │   │   ├── _enums.py             # 枚举类型，用于定义字段选项
    │   │   ├── _sqltypes.py          # 自定义 SQL 类型
    │   │   └── __init__.py           # 导入所有模型
    │   ├── views/                    # 管理员视图、运营员视图、普通用户视图
    │   │   ├── admin_views/          # 管理员视图
    │   │   │   ├── user_admin.py     # 用户管理视图
    │   │   │   ├── project_admin.py  # 项目管理视图
    │   │   │   ├── api_admin.py      # API 管理视图
    │   │   │   └── finance_admin.py  # 财务管理视图
    │   │   ├── operator_views/       # 运营专员视图
    │   │   │   ├── customer_view.py  # 客户管理视图
    │   │   │   └── revenue_view.py   # 分润统计视图
    │   │   └── user_views/           # 普通用户视图
    │   │       ├── profile_view.py   # 个人中心视图
    │   │       ├── announcement_view.py # 公告视图
    │   │       └── api_docs_view.py  # API 文档视图
    │   ├── ui_generation/            # 前端 UI 生成逻辑，确保页面按需求生成
    │   ├── utils/                    # 工具函数
    │   │   ├── functools.py          # 定义功能辅助函数
    │   │   ├── pydantic.py           # Pydantic 相关辅助函数
    │   │   └── translation.py        # 国际化支持（翻译工具）
    │   └── __init__.py               # 初始化文件

    ├── fastapi_user_auth/            # 用户认证功能，集成 GitHub 的 fastapi-user-auth
    │   ├── __init__.py               # 初始化文件
    │   ├── auth/                     # 用户认证逻辑
    │   ├── crud/                     # 认证相关的 CRUD 操作
    │   ├── models/                   # 认证模型
    │   ├── schemas/                  # 认证相关的数据模式
    │   └── utils/                    # 认证辅助函数

    ├── utils/                        # 项目通用工具函数
    │   ├── helpers.py                # 通用辅助函数
    │   ├── email_helpers.py          # 邮件相关帮助函数
    │   └── finance_helpers.py        # 财务统计帮助函数