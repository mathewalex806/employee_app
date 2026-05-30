"""
Department Service File
"""

from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import create_tables, get_db
from fastapi import Depends
from fastapi import HTTPException, status
from models.employee import Employee
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from employee.employee_repo import CreateEmployee, GetAllEmployee, GetUserById, UpdateUserByIdRepo, DeleteUserByIdRepo
from exceptions import BadRequestException, ConflictException, NotFoundException , UnauthorizedException
from auth import hash_password, verify_password, create_access_token, decode_access_token
from department.dept_repo import CreateDepartmentRepo, GetDepartmentByIdRepo, GetAllDepartmentsRepo, UpdateDepartmentByIdRepo, DeleteDepartmentByIdRepo

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


