from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi_user_auth.auth import Auth
from fastapi_user_auth.auth.models import User
from fastapi_amis_admin.admin.settings import Settings
from admin.site import CustomAdminSite
from database import get_session, init_db
from config import config
from sqlalchemy.ext.asyncio import AsyncSession
import initialize_db
import logging

logging.basicConfig(level=logging.DEBUG)

# 创建 FastAPI 应用
app = FastAPI()

# 设置跨域
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 认证系统，传入数据库连接
auth = Auth(db=get_session)

# 后台管理站点
admin_site = CustomAdminSite(
    settings=Settings(database_url=config.DATABASE_URL),
    auth=auth
)
admin_site.mount_app(app)

# 动态返回菜单配置，根据不同用户角色
@app.get("/menu_config")
async def get_menu_config(user: User = Depends(auth.get_current_user)):
    if user.role_key == "admin":
        menu_config = {
            "type": "page",
            "title": "管理员后台",
            "body": [
                {"type": "nav", "label": "用户管理", "url": "/admin/user_management"},
                {"type": "nav", "label": "邮箱管理", "url": "/admin/email_management"},
                {"type": "nav", "label": "项目管理", "url": "/admin/project_management"},
                {"type": "nav", "label": "API管理", "url": "/admin/api_management"},
                {"type": "nav", "label": "支付接口管理", "url": "/admin/payment_management"},
                {"type": "nav", "label": "财务统计", "url": "/admin/finance_statistics"},
                {"type": "nav", "label": "权限管理", "url": "/admin/permission_management"}
            ]
        }
    elif user.role_key == "operator":
        menu_config = {
            "type": "page",
            "title": "运营专员后台",
            "body": [
                {"type": "nav", "label": "客户信息管理", "url": "/operator/customer_management"},
                {"type": "nav", "label": "分润统计", "url": "/operator/revenue_statistics"}
            ]
        }
    else:
        menu_config = {
            "type": "page",
            "title": "用户后台",
            "body": [
                {"type": "nav", "label": "公告", "url": "/user/announcements"},
                {"type": "nav", "label": "个人中心", "url": "/user/profile"},
                {"type": "nav", "label": "API文档", "url": "/user/api_docs"},
                {"type": "nav", "label": "获取邮件", "url": "/user/mailbox"}
            ]
        }
    return JSONResponse(content=menu_config)

# 新增：普通用户仪表盘
@app.get("/user/dashboard")
async def user_dashboard(user: User = Depends(auth.get_current_user)):
    if user.role_key != 'user':
        raise HTTPException(status_code=403, detail="你没有权限访问用户仪表盘")
    return {"message": f"欢迎，{user.username}！这是你的用户仪表盘"}

# 新增：运营专员仪表盘
@app.get("/operator/dashboard")
async def operator_dashboard(user: User = Depends(auth.get_current_user)):
    if user.role_key != 'operator':
        raise HTTPException(status_code=403, detail="你没有权限访问运营专员仪表盘")
    return {"message": f"欢迎，{user.username}！这是你的运营专员仪表盘"}

# 新增：管理员仪表盘
@app.get("/admin/dashboard")
async def admin_dashboard(user: User = Depends(auth.get_current_user)):
    if user.role_key != 'admin':
        raise HTTPException(status_code=403, detail="你没有权限访问管理员仪表盘")
    return {"message": f"欢迎，{user.username}！这是你的管理员仪表盘"}

# 初始化数据库
@app.on_event("startup")
async def startup_event():
    await initialize_db.init_db()

# 运行主应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
