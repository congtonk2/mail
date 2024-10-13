from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from typing import AsyncGenerator
from config import config  # 引入 config.py

# 使用 config 中的 DATABASE_URL
DATABASE_URL = config.DATABASE_URL

# 创建异步引擎
engine = create_async_engine(DATABASE_URL, echo=True)

# 创建 sessionmaker
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话对象
    """
    async with async_session() as session:
        yield session

async def init_db():
    """
    初始化数据库，创建所有表
    """
    async with engine.begin() as conn:
        # 先检查表是否存在，再创建表
        await conn.run_sync(SQLModel.metadata.create_all)
