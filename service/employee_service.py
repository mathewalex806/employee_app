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
import repository.employee_repo as emp_repo

async def create(db: AsyncSession, name: str, email:str) -> Employee:
    if not isinstance(name, str) or not name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must not be empty")
    if not isinstance(email, str) or not email.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must not be empty")
    
    employee = await emp_repo.CreateEmployee(db=db, name=name, email=email)
    return employee


async def GetAllUsers(db:AsyncSession):
    users = await emp_repo.GetAllEmployee(db=db)
    return users


async def GetUserById(id:int, db:AsyncSession):
    if not isinstance(id, int) or id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="id field is invalid")
    user = await emp_repo.GetUserById(id=id, db=db)
    return user


async def UpdateUserByIdService(db: AsyncSession, name: str, email:str, id:int) -> Employee:
    if not isinstance(name, str) or not name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must not be empty")
    if not isinstance(email, str) or not email.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must not be empty")
    if not isinstance(id, int) or id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Id must not be empty")
    
    updatedEmployee = await emp_repo.UpdateUserByIdRepo(id=id, name=name, email=email, db=db)
    return updatedEmployee


async def DeleteUserByIdService(id:int, db: AsyncSession):
    if not isinstance(id, int) or id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Id must not be empty")
    
    deleted_employee = await emp_repo.DeleteUserByIdRepo(id=id, db=db)
    return deleted_employee