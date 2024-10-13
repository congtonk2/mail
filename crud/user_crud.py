# crud/user_crud.py

from fastapi_user_auth.auth.models import MyUser
from fastapi_amis_admin.crud import BaseCrud
from sqlmodel import select
from fastapi_user_auth.auth import Auth
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


class UserCrud(BaseCrud[MyUser]):
    """用户相关的 CRUD 操作"""

    def __init__(self, auth: Auth):
        super().__init__(model=MyUser)  # 使用自定义的用户模型
        self.auth = auth  # 引入 Auth 对象用于用户认证和授权

    async def create_user(self, session: AsyncSession, username: str, password: str, role_key: str = 'user'):
        """
        创建新用户并分配角色
        :param session: 数据库 session
        :param username: 用户名
        :param password: 用户密码
        :param role_key: 角色标识符，默认为普通用户（'user')
        """
        if await self.auth.get_user_by_username(username):
            raise ValueError("用户已存在")

        # 使用 auth 创建用户并分配角色
        await self.auth.create_role_user(username=username, password=password, role_key=role_key)
        return {"message": f"用户 {username} 创建成功，角色：{role_key}"}

    async def update_user(self, session: AsyncSession, user_id: int, data: dict):
        """
        更新用户信息
        :param session: 数据库 session
        :param user_id: 用户ID
        :param data: 更新字段的字典
        """
        user = await session.get(MyUser, user_id)
        if not user:
            raise ValueError("用户不存在")

        for field, value in data.items():
            setattr(user, field, value)
        await session.commit()
        return {"message": f"用户 {user.username} 更新成功"}

    async def delete_user(self, session: AsyncSession, user_id: int):
        """
        删除用户
        :param session: 数据库 session
        :param user_id: 用户ID
        """
        user = await session.get(MyUser, user_id)
        if not user:
            raise ValueError("用户不存在")

        await session.delete(user)
        await session.commit()
        return {"message": f"用户 {user.username} 删除成功"}

    async def get_user_by_username(self, session: AsyncSession, username: str):
        """
        根据用户名获取用户，并添加异常处理
        :param session: 数据库 session
        :param username: 用户名
        """
        try:
            statement = select(MyUser).where(MyUser.username == username)
            result = await session.execute(statement)
            user = result.scalars().first()
            if not user:
                raise ValueError(f"用户 {username} 不存在")
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"查询用户失败: {str(e)}")