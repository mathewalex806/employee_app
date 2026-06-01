"""
Auth Service file
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.utils import create_access_token, verify_password
from exceptions.handlers import UnauthorizedException
from models.employee import Employee


# async def login(db:AsyncSession, email: str) -> Employee | None:
#     query =   select(Employee).where(Employee.email == email, Employee.deleted_at.is_(None))
#     employee =  await db.scalars(query)
#     return employee.first()


async def login(db: AsyncSession, email: str, password: str) -> str:

    query = select(Employee).where(
        Employee.email == email, Employee.deleted_at.is_(None)
    )

    result = await db.scalars(query)
    employee = result.first()

    if employee is None:
        raise UnauthorizedException("Invalid credentials")

    if not verify_password(plain=password, hashed=employee.password_hash):
        raise UnauthorizedException("Invalid credentials")

    token = create_access_token(
        {"sub": str(employee.id), "email": employee.email, "role": employee.role.value}
    )

    return token
