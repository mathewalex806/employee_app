"""
Employee repo
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database.connection import create_tables, get_db
from fastapi import Depends
from fastapi import HTTPException, status
from models.address import Address
from models.employee import Employee
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from exceptions import NotFoundException, BadRequestException, ConflictException
from models import Department

async def CreateEmployee(name: str, email: str, password : str,db: AsyncSession)-> Employee:
    db_employee = Employee(name=name, email= email, password_hash = password)
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



async def AddEmployeeToDepartment(emp_id: int, dept_id : int, db : AsyncSession):
    employee_query = select(Employee).where(Employee.id == emp_id)
    department_query = select(Department).where(Department.id == dept_id)

    employee_result = await db.scalars(employee_query)


    employee = employee_result.first()


    department_result = await db.scalars(department_query)
    department = department_result.first()

    if employee is None:
        raise NotFoundException("Employee not found")
    if department is None:
        raise NotFoundException("Department not found")
    
    employee.departments.append(department)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise BadRequestException("Employee is already in the department")

    await db.refresh(employee)
    return employee


async def DeleteEmployeeFromDepartment(emp_id: int, dept_id :int , db = AsyncSession):
    employee_query = select(Employee).where(Employee.id == emp_id)
    department_query = select(Department).where(Department.id == dept_id)

    employee_result = await db.scalars(employee_query)
    employee = employee_result.first()

    department_result = await db.scalars(department_query)
    department = department_result.first()

    if employee is None:
        raise NotFoundException("Employee not found")
    if department is None:
        raise NotFoundException("Department not found")
    
    if department not in employee.departments:
        raise BadRequestException("Employee is not in the department")
    
    employee.departments.remove(department)

    try:
        await db.commit()
    except Exception as e:
        print(e)
        await db.rollback()
        raise BadRequestException("Operation failed")

    await db.refresh(employee)
    return employee


async def AddUserAddress(emp_id : int, address_data : dict, db : AsyncSession):
    employee_query = select(Employee).where(Employee.id == emp_id)
    employee_result = await db.scalars(employee_query)
    empolyee = employee_result.first()
    if empolyee is None:
        raise NotFoundException("Employee not found")
    
    address = Address(
        line_1 = address_data.get("line1", None),
        city = address_data.get("city", None),
        postal_code = int(address_data.get("postal_code", None)),
        country = address_data.get("country", None),
        employee_id = emp_id

    )
    empolyee.addresses.append(address)

    try:
        await db.commit()
    except Exception as e:
        print(e)
        await db.rollback()
        raise BadRequestException("Failed to add address")
    await db.refresh(empolyee)
    return empolyee


async def UpdateUserAddress(emp_id: int,address_id: int,address_data: dict,db: AsyncSession):
    query = (select(Address).where(Address.id == address_id,Address.employee_id == emp_id))

    result = await db.scalars(query)
    address = result.first()

    if address is None:
        raise NotFoundException("Address not found")

    if "line1" in address_data:
        address.line_1 = address_data["line1"]

    if "city" in address_data:
        address.city = address_data["city"]

    if "postal_code" in address_data:
        address.postal_code = (
            int(address_data["postal_code"])
            if address_data["postal_code"] is not None
            else None
        )

    if "country" in address_data:
        address.country = address_data["country"]

    try:
        await db.commit()
        await db.refresh(address)
    except Exception:
        await db.rollback()
        raise BadRequestException("Failed to update address")

    return address


async def SoftDeleteUserAddress(
    emp_id: int,
    address_id: int,
    db: AsyncSession
):
    query = (
        select(Address)
        .where(
            Address.id == address_id,
            Address.employee_id == emp_id,
            Address.deleted_at.is_(None)
        )
    )

    result = await db.scalars(query)
    address = result.first()

    if address is None:
        raise NotFoundException("Address not found")

    address.deleted_at = datetime.now(timezone.utc)

    try:
        await db.commit()
        await db.refresh(address)
    except Exception:
        await db.rollback()
        raise BadRequestException("Failed to delete address")

    return {
        "message": "Address deleted successfully",
        "address_id": address.id
    }