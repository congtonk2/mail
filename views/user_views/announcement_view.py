from fastapi_amis_admin.admin import ModelAdmin, PageSchema
from models.announcement import Announcement  # 假设有公告模型
from crud.announcement_crud import AnnouncementCrud  # 假设有公告 CRUD 操作
from cachetools import TTLCache
import logging

# 创建一个缓存，存储100条记录，TTL（缓存有效期）为60秒
announcement_cache = TTLCache(maxsize=100, ttl=60)

# 日志配置
logging.basicConfig(
    filename='app.log',  # 日志文件
    filemode='a',  # 追加模式
    level=logging.INFO,  # 记录INFO及以上日志
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AnnouncementView(ModelAdmin):
    """
    普通用户查看公告的视图
    """
    page_schema = PageSchema(label="系统公告", icon="fa fa-bullhorn")
    model = Announcement
    list_display = ["title", "content", "created_at"]  # 显示公告的标题、内容、创建时间
    list_filter = ["created_at"]  # 可以根据创建时间过滤公告

    def __init__(self, announcement_crud: AnnouncementCrud):
        super().__init__()
        self.announcement_crud = announcement_crud

    async def get_announcements(self):
        """
        获取所有公告，优先从缓存获取；按创建时间倒序排列
        """
        try:
            # 检查缓存
            if "announcements" in announcement_cache:
                logging.info("从缓存中获取公告列表")
                return announcement_cache["announcements"]
            
            # 从数据库获取公告列表
            logging.info("从数据库中获取公告列表")
            announcements = await self.announcement_crud.get_all_announcements(order_by="created_at desc")

            # 将公告列表缓存
            announcement_cache["announcements"] = announcements
            return announcements
        except Exception as e:
            logging.error(f"获取公告列表失败: {str(e)}")
            raise HTTPException(status_code=500, detail="获取公告列表失败")
