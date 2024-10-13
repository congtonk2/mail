# crud/project_crud.py

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.project import Project

class ProjectCrud:
    """项目的 CRUD 操作"""

    async def create_project(self, session: AsyncSession, data: dict) -> Project:
        """
        创建新项目
        :param session: 数据库会话
        :param data: 项目数据
        :return: 新创建的项目
        """
        new_project = Project(**data)
        session.add(new_project)
        await session.commit()
        await session.refresh(new_project)
        return new_project

    async def get_project_by_code(self, session: AsyncSession, code: str) -> Project:
        """
        根据项目代码获取项目
        :param session: 数据库会话
        :param code: 项目代码
        :return: 项目
        """
        statement = select(Project).where(Project.code == code)
        result = await session.execute(statement)
        return result.scalars().first()

    async def update_project(self, session: AsyncSession, project_id: int, data: dict) -> Project:
        """
        更新项目信息
        :param session: 数据库会话
        :param project_id: 项目ID
        :param data: 项目更新的数据
        :return: 更新后的项目
        """
        project = await session.get(Project, project_id)
        if project:
            for key, value in data.items():
                setattr(project, key, value)
            await session.commit()
            await session.refresh(project)
        return project

    async def delete_project(self, session: AsyncSession, project_id: int):
        """
        删除项目
        :param session: 数据库会话
        :param project_id: 项目ID
        """
        project = await session.get(Project, project_id)
        if project:
            await session.delete(project)
            await session.commit()

    async def get_all_projects(self, session: AsyncSession) -> list[Project]:
        """
        获取所有项目
        :param session: 数据库会话
        :return: 项目列表
        """
        statement = select(Project)
        result = await session.execute(statement)
        return result.scalars().all()
