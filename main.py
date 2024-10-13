from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi_user_auth.auth import Auth
from fastapi_user_auth.auth.models import User
from fastapi_amis_admin.admin.settings import Settings
from admin.site import CustomAdminSite
from database import get_session, async_session, init_db  # Updated session management
from config import config
from sqlalchemy.ext.asyncio import AsyncSession
import initialize_db

import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

# Create FastAPI app
app = FastAPI()

# Set CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Auth with session
auth = Auth(db=async_session)

# Admin site setup
admin_site = CustomAdminSite(
    settings=Settings(database_url=config.DATABASE_URL),
    auth=auth
)
admin_site.mount_app(app)

# Menu configuration based on user role
@app.get("/menu_config")
async def get_menu_config(user: User = Depends(auth.get_current_user)):
    if user.role_key == "admin":
        menu_config = {
            "type": "page",
            "title": "Admin Dashboard",
            "body": [
                {"type": "nav", "label": "User Management", "url": "/admin/user_management"},
                {"type": "nav", "label": "Email Management", "url": "/admin/email_management"},
                {"type": "nav", "label": "Project Management", "url": "/admin/project_management"},
                {"type": "nav", "label": "API Management", "url": "/admin/api_management"},
                {"type": "nav", "label": "Payment Management", "url": "/admin/payment_management"},
                {"type": "nav", "label": "Finance Statistics", "url": "/admin/finance_statistics"},
                {"type": "nav", "label": "Permission Management", "url": "/admin/permission_management"}
            ]
        }
    elif user.role_key == "operator":
        menu_config = {
            "type": "page",
            "title": "Operator Dashboard",
            "body": [
                {"type": "nav", "label": "Customer Management", "url": "/operator/customer_management"},
                {"type": "nav", "label": "Revenue Statistics", "url": "/operator/revenue_statistics"}
            ]
        }
    else:
        menu_config = {
            "type": "page",
            "title": "User Dashboard",
            "body": [
                {"type": "nav", "label": "Announcements", "url": "/user/announcements"},
                {"type": "nav", "label": "Profile", "url": "/user/profile"},
                {"type": "nav", "label": "API Docs", "url": "/user/api_docs"},
                {"type": "nav", "label": "Mailbox", "url": "/user/mailbox"}
            ]
        }
    return JSONResponse(content=menu_config)

# Dashboard endpoints based on user role
@app.get("/user/dashboard")
async def user_dashboard(user: User = Depends(auth.get_current_user)):
    if user.role_key != 'user':
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"message": f"Welcome {user.username}, to your user dashboard"}

@app.get("/operator/dashboard")
async def operator_dashboard(user: User = Depends(auth.get_current_user)):
    if user.role_key != 'operator':
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"message": f"Welcome {user.username}, to your operator dashboard"}

@app.get("/admin/dashboard")
async def admin_dashboard(user: User = Depends(auth.get_current_user)):
    if user.role_key != 'admin':
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"message": f"Welcome {user.username}, to your admin dashboard"}

# Initialize the database on startup
@app.on_event("startup")
async def startup_event():
    await initialize_db.init_db()

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
