"""
Employee service
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


async def create(db: AsyncSession, name: str, email:str, password:str) -> Employee:
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException("Name should not be empty")
    if not isinstance(email, str) or not email.strip():
        raise BadRequestException("Email should not be empty")
    if not isinstance(password, str) or not password.strip():
        raise BadRequestException("Password Field should not be empty")
    
    hashed_password = hash_password(password)
    
    employee = await CreateEmployee(db=db, name=name, email=email, password = hashed_password)
    return employee


async def GetAllUsers(db:AsyncSession):
    users = await GetAllEmployee(db=db)
    return users


async def GetUserByIdService(id:int, db: AsyncSession):
    user = await GetUserById(id=id, db=db)
    return user


async def UpdateUserByIdService(db: AsyncSession, name: str, email:str, id:int) -> Employee:
    if not isinstance(name, str) or not name.strip():
        raise 
    if not isinstance(email, str) or not email.strip():
        raise BadRequestException("Email should not be empty")
    if not isinstance(id, int) or id is None:
        raise BadRequestException("ID should not be empty")
    
    updatedEmployee = await UpdateUserByIdRepo(id=id, name=name, email=email, db=db)
    return updatedEmployee


async def DeleteUserByIdService(id:int, db: AsyncSession):
    if not isinstance(id, int) or id is None:
        raise BadRequestException("ID should not be empty")
    
    deleted_employee = await DeleteUserByIdRepo(id=id, db=db)
    return deleted_employee



