"""
Employee repo
"""
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import create_tables, get_db
from fastapi import Depends
from fastapi import HTTPException, status
from models.employee import Employee
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from exceptions import NotFoundException, BadRequestException, ConflictException

async def CreateEmployee(name: str, email: str, db: AsyncSession)-> Employee:
    db_employee = Employee(name=name, email= email)
    db.add(db_employee)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException("Email already in use")
    await db.refresh(db_employee)
    return db_employee

async def GetAllEmployee(db:AsyncSession = AsyncSession):
    query = select(Employee).where(Employee.deleted_at.is_(None))
    result = await db.scalars(query)
    return result.all()


async def GetUserById(id:int, db:AsyncSession):
    query = select(Employee).where(Employee.id == id)
    
    result = await db.scalars(query)
    employee = result.first()
    if result is None or employee is None:
        raise NotFoundException("Employee not found")
    return employee


async def UpdateUserByIdRepo(id:int, name: str,email: str,db:AsyncSession):
    query = select(Employee).where(Employee.id == id)
    result = await db.scalars(query)
    employee = result.first()
    if employee is None:
        raise NotFoundException("User not found")
    employee.name= name
    employee.email = email

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise BadRequestException("Failed to update employee")
    await db.refresh(employee)
    return employee


async def DeleteUserByIdRepo(id:int, db:AsyncSession):
    query = select(Employee).where(Employee.id == id)
    result = await db.scalars(query)
    employee = result.first()
    if employee is None:
        raise NotFoundException("User not found")
    if employee.deleted_at is not None:
        return {"message":"Employee does not exist"}
    employee.deleted_at = datetime.now(timezone.utc)
    
    try:
        await db.commit()
    except Exception as e:
        print(e)
        await db.rollback()

        raise BadRequestException("Operation failed")
    await db.refresh(employee)
    return {"message":"Record Deleted"}




