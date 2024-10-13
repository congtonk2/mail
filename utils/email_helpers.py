# utils/email_helpers.py

import re
from typing import List, Dict
from models.email import EmailResource, ChildEmail
from sqlalchemy.ext.asyncio import AsyncSession

def validate_email_format(email: str) -> bool:
    """
    验证邮箱地址的格式是否正确
    """
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email) is not None

async def get_available_parent_email(session: AsyncSession) -> List[EmailResource]:
    """
    获取所有可用的父邮箱（状态为 'available' 的邮箱）
    """
    return await session.execute("SELECT * FROM emailresource WHERE status = 'available'")

async def generate_child_emails(parent_email: EmailResource, project_code: str, num_emails: int) -> List[ChildEmail]:
    """
    从父邮箱生成指定数量的子邮箱
    :param parent_email: 父邮箱对象
    :param project_code: 项目代码
    :param num_emails: 需要生成的子邮箱数量
    :return: 生成的子邮箱列表
    """
    child_emails = []
    for i in range(num_emails):
        generated_email = f"{i+1}.{parent_email.parent_email}"  # 根据父邮箱生成子邮箱地址
        child_email = ChildEmail(
            parent_email_id=parent_email.email_id,
            generated_email=generated_email,
            project_code=project_code,
            status="unused"  # 子邮箱初始状态为未使用
        )
        child_emails.append(child_email)
    return child_emails

async def update_parent_email_status(session: AsyncSession, parent_email_id: int, status: str) -> None:
    """
    更新父邮箱的状态
    :param session: 数据库 session
    :param parent_email_id: 父邮箱ID
    :param status: 更新后的状态 (available, disabled, banned)
    """
    await session.execute(f"UPDATE emailresource SET status = '{status}' WHERE email_id = {parent_email_id}")
    await session.commit()

async def update_child_email_usage(session: AsyncSession, child_email: ChildEmail, project_code: str) -> None:
    """
    更新子邮箱的使用情况
    :param session: 数据库 session
    :param child_email: 子邮箱对象
    :param project_code: 当前项目代码
    """
    child_email.status = "used"
    child_email.completed_projects[project_code] = True  # 标记该项目为已完成
    await session.commit()
