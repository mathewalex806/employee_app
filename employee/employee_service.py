"""
Employee service
"""

from sqlalchemy.ext.asyncio import AsyncSession
from models.employee import Employee, EmployeeRole, Status
from employee.employee_repo import (
    CreateEmployee,
    GetAllEmployee,
    GetUserById,
    GetUsersByStatus,
    UpdateUserByIdRepo,
    DeleteUserByIdRepo,
    AddEmployeeToDepartment,
    DeleteEmployeeFromDepartment,
    AddUserAddress,
    UpdateUserAddress,
    SoftDeleteUserAddress,
)
from exceptions import BadRequestException
from auth import hash_password
from employee.schemas import AddressCreate


async def create(
    db: AsyncSession,
    name: str,
    email: str,
    password: str,
    role: str,
    age: int,
    address: AddressCreate,
    status: Status,
    exp: str,
) -> Employee:
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException("Name should not be empty")
    if not isinstance(email, str) or not email.strip():
        raise BadRequestException("Email should not be empty")
    if not isinstance(password, str) or not password.strip():
        raise BadRequestException("Password Field should not be empty")

    hashed_password = hash_password(password)

    employee = await CreateEmployee(
        db=db,
        name=name,
        email=email,
        password=hashed_password,
        role=role,
        age=age,
        address=address,
        status=status,
        exp=exp,
    )
    return employee


async def GetAllUsers(db: AsyncSession):
    users = await GetAllEmployee(db=db)
    return users


async def GetUserByIdService(id: int, db: AsyncSession):
    user = await GetUserById(id=id, db=db)
    return user


async def UpdateUserByIdService(
    db: AsyncSession,
    name: str,
    email: str,
    id: int,
    age: int,
    role: EmployeeRole,
    status: Status,
    experience: str,
) -> Employee:
    if not isinstance(name, str) or not name.strip():
        raise
    if not isinstance(email, str) or not email.strip():
        raise BadRequestException("Email should not be empty")
    if not isinstance(id, int) or id is None:
        raise BadRequestException("ID should not be empty")

    if not isinstance(age, int) or age is None:
        raise BadRequestException("Age should not be empty")

    if not isinstance(role, EmployeeRole) or role is None:
        raise BadRequestException("Employee role should not be empty")

    updatedEmployee = await UpdateUserByIdRepo(
        id=id,
        name=name,
        email=email,
        db=db,
        age=age,
        role=role,
        status=status,
        experience=experience,
    )
    return updatedEmployee


async def DeleteUserByIdService(id: int, db: AsyncSession):
    if not isinstance(id, int) or id is None:
        raise BadRequestException("ID should not be empty")

    deleted_employee = await DeleteUserByIdRepo(id=id, db=db)
    return deleted_employee


async def AddEmployeeToDepartmentService(emp_id: int, dept_id: int, db: AsyncSession):
    if not isinstance(emp_id, int) or emp_id is None:
        raise BadRequestException("Employee ID should not be empty")
    if not isinstance(dept_id, int) or dept_id is None:
        raise BadRequestException("Department ID should not be empty")

    result = await AddEmployeeToDepartment(emp_id=emp_id, dept_id=dept_id, db=db)
    return result


async def DeleteEmployeeFromDepartmentService(
    emp_id: int, dept_id: int, db: AsyncSession
):
    if not isinstance(emp_id, int) or emp_id is None:
        raise BadRequestException("Employee ID should not be empty")
    if not isinstance(dept_id, int) or dept_id is None:
        raise BadRequestException("Department ID should not be empty")

    result = await DeleteEmployeeFromDepartment(emp_id=emp_id, dept_id=dept_id, db=db)
    return result


async def AddUserAddressService(emp_id: int, address_data: dict, db: AsyncSession):
    if not isinstance(emp_id, int) or emp_id is None:
        raise BadRequestException("Employee ID should not be empty")
    if not isinstance(address_data, dict) or not address_data:
        raise BadRequestException("Address data should not be empty")

    result = await AddUserAddress(emp_id=emp_id, address_data=address_data, db=db)
    return result


async def UpdateAddressService(
    emp_id: int, address_data: dict, address_id: int, db: AsyncSession
):
    if not isinstance(emp_id, int) or emp_id is None:
        raise BadRequestException("Employee ID should not be empty")
    if not isinstance(address_data, dict) or not address_data:
        raise BadRequestException("Address data should not be empty")
    if not isinstance(address_id, int) or address_id is None:
        raise BadRequestException("Address ID should not be empty")

    result = await UpdateUserAddress(
        emp_id=emp_id, address_data=address_data, address_id=address_id, db=db
    )
    return result


async def DeleteAddressService(emp_id: int, address_id: int, db: AsyncSession):
    result = await SoftDeleteUserAddress(emp_id=emp_id, address_id=address_id, db=db)

    return result


async def GetUsersByStatusService(status: Status, db: AsyncSession):
    result = await GetUsersByStatus(status=status, db=db)

    return result
