# config.py

from pydantic import BaseSettings

class Config(BaseSettings):
    # 应用配置
    APP_NAME: str = "FastAPI Amis Admin"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./amisadmin.db"  # 修改为你的数据库URL

    # JWT 配置
    JWT_SECRET_KEY: str = "pfAVcSq4bSeRt4f_Vs-w_ZpYLRPSdvszcV38VLjDkhc"  # 用于签发 JWT 的密钥
    JWT_ALGORITHM: str = "HS256"  # 使用的算法
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 访问 token 的有效期（分钟）

    class Config:
        env_file = ".env"  # 从 .env 文件中读取配置

config = Config()
