# crud/announcement_crud.py

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.announcement import Announcement

class AnnouncementCrud:
    """公告的 CRUD 操作"""

    async def get_all_announcements(self, session: AsyncSession, order_by: str = "created_at desc") -> 'list[Announcement]':
        """
        获取所有公告，按创建时间倒序排列
        :param session: 数据库会话
        :param order_by: 排序字段
        :return: 公告列表
        """
        statement = select(Announcement).order_by(order_by)
        result = await session.execute(statement)
        return result.scalars().all()

    async def create_announcement(self, session: AsyncSession, data: dict) -> Announcement:
        """
        创建新公告
        :param session: 数据库会话
        :param data: 公告数据
        :return: 新创建的公告
        """
        new_announcement = Announcement(**data)
        session.add(new_announcement)
        await session.commit()
        await session.refresh(new_announcement)
        return new_announcement
