"""
Department Service File
"""

from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import BadRequestException
from department.dept_repo import (
    CreateDepartmentRepo,
    GetDepartmentByIdRepo,
    GetAllDepartmentsRepo,
    UpdateDepartmentByIdRepo,
    DeleteDepartmentByIdRepo,
)


async def CreateDepartmentService(db: AsyncSession, name: str):
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException("Name should not be empty")

    # Implementation for creating department
    return await CreateDepartmentRepo(name=name, db=db)


async def GetDepartmentByIdService(id: int, db: AsyncSession):
    if not isinstance(id, int) or id is None:
        raise BadRequestException("ID should not be empty")
    return await GetDepartmentByIdRepo(id=id, db=db)


async def GetAllDepartments(db: AsyncSession):
    return await GetAllDepartmentsRepo(db=db)


async def UpdateDepartmentByIdService(id: int, name: str, db: AsyncSession):
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException("Name should not be empty")
    if not isinstance(id, int) or id is None:
        raise BadRequestException("ID should not be empty")

    return await UpdateDepartmentByIdRepo(id=id, name=name, db=db)


async def DeleteDepartmentByIdService(id: int, db: AsyncSession):
    if not isinstance(id, int) or id is None:
        raise BadRequestException("ID should not be empty")

    return await DeleteDepartmentByIdRepo(id=id, db=db)
