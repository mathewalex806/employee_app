"""
Department Repository containing all database operations for Department entity.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from exceptions import NotFoundException, BadRequestException, ConflictException
from models.department import Department


async def CreateDepartmentRepo(name: str, db: AsyncSession):

    department = Department(name=name)
    db.add(department)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException("Department with this name already exists")
    await db.refresh(department)
    return department


async def GetDepartmentByIdRepo(id: int, db: AsyncSession):
    query = select(Department).where(Department.id == id)
    result = await db.scalars(query)
    department = result.first()
    if department is None:
        raise NotFoundException("Department not found")
    return department


async def GetAllDepartmentsRepo(db: AsyncSession):
    query = select(Department).where(Department.deleted_at.is_(None))
    result = await db.scalars(query)
    return result.all()


async def UpdateDepartmentByIdRepo(id: int, name: str, db: AsyncSession):
    query = select(Department).where(Department.id == id)
    result = await db.scalars(query)
    department = result.first()

    if department is None:
        raise NotFoundException("Department not found")

    department.name = name

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise BadRequestException("Failed to update department")
    await db.refresh(department)
    return department


async def DeleteDepartmentByIdRepo(id: int, db: AsyncSession):
    query = select(Department).where(Department.id == id)
    result = await db.scalars(query)
    department = result.first()
    if department is None:
        raise NotFoundException("Department not found")
    if department.deleted_at is not None:
        raise BadRequestException("Record does not exist")
    department.deleted_at = datetime.now(timezone.utc)
    await db.commit()
    return department
