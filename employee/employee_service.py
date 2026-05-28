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

async def create(db: AsyncSession, name: str, email:str) -> Employee:
    if not isinstance(name, str) or not name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must not be empty")
    if not isinstance(email, str) or not email.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must not be empty")
    
    employee = await CreateEmployee(db=db, name=name, email=email)
    return employee


async def GetAllUsers(db:AsyncSession):
    users = await GetAllEmployee(db=db)
    return users


async def GetUserByIdService(id:int, db: AsyncSession):
    user = await GetUserById(id=id, db=db)
    return user


async def UpdateUserByIdService(db: AsyncSession, name: str, email:str, id:int) -> Employee:
    if not isinstance(name, str) or not name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must not be empty")
    if not isinstance(email, str) or not email.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must not be empty")
    if not isinstance(id, int) or id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Id must not be empty")
    
    updatedEmployee = await UpdateUserByIdRepo(id=id, name=name, email=email, db=db)
    return updatedEmployee


async def DeleteUserByIdService(id:int, db: AsyncSession):
    if not isinstance(id, int) or id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Id must not be empty")
    
    deleted_employee = await DeleteUserByIdRepo(id=id, db=db)
    return deleted_employee