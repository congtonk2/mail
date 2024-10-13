from sqlmodel import select
from models.email import EmailResource, ChildEmail
from fastapi_amis_admin.crud import BaseCrud
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from utils.functools import logger  # 假设已经设置了一个简单的日志功能

class EmailCrud(BaseCrud[EmailResource]):
    """父邮箱和子邮箱相关的 CRUD 操作"""

    def __init__(self):
        super().__init__(model=EmailResource)  # 父邮箱的基础 CRUD 操作

    async def create_parent_email(self, session: AsyncSession, parent_email: str, parent_password: str, smtp_email: str, smtp_password: str):
        """
        创建父邮箱，添加异常处理和日志记录
        """
        try:
            email_resource = EmailResource(
                parent_email=parent_email,
                parent_password=parent_password,
                smtp_email=smtp_email,
                smtp_password=smtp_password,
                status="available"  # 默认父邮箱状态为 "available"
            )
            session.add(email_resource)
            await session.commit()
            logger.info(f"创建父邮箱 {parent_email}")
            return {"message": "父邮箱创建成功", "email_id": email_resource.email_id}
        except Exception as e:
            logger.error(f"创建父邮箱失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"创建父邮箱失败: {str(e)}")

    async def update_parent_email(self, session: AsyncSession, email_id: int, data: dict):
        """
        更新父邮箱信息，添加异常处理
        """
        try:
            email_resource = await session.get(EmailResource, email_id)
            if not email_resource:
                raise ValueError("父邮箱不存在")

            for field, value in data.items():
                setattr(email_resource, field, value)
            await session.commit()
            logger.info(f"更新父邮箱 {email_resource.parent_email}")
            return {"message": f"父邮箱 {email_resource.parent_email} 更新成功"}
        except Exception as e:
            logger.error(f"更新父邮箱失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"更新父邮箱失败: {str(e)}")

    async def delete_parent_email(self, session: AsyncSession, email_id: int):
        """
        删除父邮箱，添加异常处理
        """
        try:
            email_resource = await session.get(EmailResource, email_id)
            if not email_resource:
                raise ValueError("父邮箱不存在")

            await session.delete(email_resource)
            await session.commit()
            logger.info(f"删除父邮箱 {email_resource.parent_email}")
            return {"message": f"父邮箱 {email_resource.parent_email} 删除成功"}
        except Exception as e:
            logger.error(f"删除父邮箱失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"删除父邮箱失败: {str(e)}")

    async def create_child_email(self, session: AsyncSession, parent_email_id: int, generated_email: str, project_code: str):
        """
        生成子邮箱，并确保地址唯一，添加异常处理和日志记录
        """
        try:
            parent_email = await session.get(EmailResource, parent_email_id)
            if not parent_email:
                raise ValueError("父邮箱不存在")

            # 检查生成的子邮箱是否唯一
            existing_email = await session.execute(select(ChildEmail).where(ChildEmail.generated_email == generated_email))
            if existing_email.scalars().first():
                raise HTTPException(status_code=400, detail=f"子邮箱 {generated_email} 已存在")

            child_email = ChildEmail(
                parent_email_id=parent_email_id,
                generated_email=generated_email,
                project_code=project_code,
                status="unused"  # 默认状态为未使用
            )
            session.add(child_email)
            await session.commit()
            logger.info(f"创建子邮箱 {generated_email}")
            return {"message": "子邮箱创建成功", "child_email_id": child_email.child_email_id}
        except Exception as e:
            logger.error(f"创建子邮箱失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"创建子邮箱失败: {str(e)}")

    async def get_child_emails(self, session: AsyncSession, parent_email_id: int) -> List[ChildEmail]:
        """
        获取父邮箱下的所有子邮箱，添加错误处理
        """
        try:
            statement = select(ChildEmail).where(ChildEmail.parent_email_id == parent_email_id)
            result = await session.execute(statement)
            child_emails = result.scalars().all()
            if not child_emails:
                raise ValueError(f"父邮箱 {parent_email_id} 下没有子邮箱")
            return child_emails
        except Exception as e:
            logger.error(f"获取子邮箱失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"获取子邮箱失败: {str(e)}")

    async def update_child_email_status(self, session: AsyncSession, child_email_id: int, status: str):
        """
        更新子邮箱的状态，添加异常处理和日志记录
        """
        try:
            child_email = await session.get(ChildEmail, child_email_id)
            if not child_email:
                raise ValueError("子邮箱不存在")

            child_email.status = status
            await session.commit()
            logger.info(f"更新子邮箱状态为 {status}, 子邮箱: {child_email.generated_email}")
            return {"message": f"子邮箱 {child_email.generated_email} 的状态已更新为 {status}"}
        except Exception as e:
            logger.error(f"更新子邮箱状态失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"更新子邮箱状态失败: {str(e)}")
