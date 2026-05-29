
"""
Auth Service file
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.employee import Employee


async def login(db:AsyncSession, email: str) -> Employee | None:
    query =   select(Employee).where(Employee.email == email, Employee.deleted_at.is_(None))
    employee =  await db.scalars(query)
    return employee.first()
