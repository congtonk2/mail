import asyncio
from database import init_db, engine
from sqlmodel import SQLModel
import logging

# 设置日志
logging.basicConfig(
    filename='db_init.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def init():
    """
    运行数据库初始化，创建所有表
    """
    try:
        # 确认数据库连接并创建所有表
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logging.info("数据库初始化成功，所有表已创建")

    except Exception as e:
        logging.error(f"数据库初始化失败: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(init())
