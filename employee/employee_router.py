"""
Employee Router
"""


from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import create_tables, get_db
from fastapi import Depends
from fastapi import HTTPException, status

from fastapi import APIRouter, Body

import employee.employee_service as emp_service
from employee.schemas import EmployeeCreate, AddressCreate, EmployeeResponse, EmployeeResponseByUserId , AddressResponse , EmployeeResponseAddress
from auth.dependencies import get_current_user
from auth.schemas import TokenPayload

router = APIRouter(prefix="/api/v1", tags=["Employee"])

@router.get("/health", status_code = status.HTTP_200_OK)
def health():
    return {
        "message": "Server is healthy"
    }

@router.post("/employee", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
async def create_employee(body: EmployeeCreate, db:AsyncSession = Depends(get_db)):
    name = body.name
    email = body.email
    password = body.password

    employee =  await emp_service.create(db=db, name=name, email=email, password=password)
    return employee


@router.get("/users", status_code=status.HTTP_200_OK, response_model= list[EmployeeResponse])
async def GetUsers(db:AsyncSession = Depends(get_db), _current_user : TokenPayload = Depends(get_current_user)):
    name = "Alex"
    print(f"{name}")
    employees = await emp_service.GetAllUsers(db=db)
    return employees

@router.get("/user/{id}", status_code=status.HTTP_200_OK, response_model= EmployeeResponseAddress)
async def GetUserById(id:int, db:AsyncSession = Depends(get_db)):
    employee = await emp_service.GetUserById(id=id, db=db)
    return employee


@router.put("/user/{id}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse)
async def UpdateUserById(id:int, body  : EmployeeCreate, db:AsyncSession = Depends(get_db)):
    name = body.name
    email = body.email
    

    updated_employee = await emp_service.UpdateUserByIdService(db=db, name=name, email=email, id=id)
    return updated_employee


@router.delete("/user/{id}", status_code=status.HTTP_200_OK)
async def DeleteUserById(id:int, db:AsyncSession = Depends(get_db)):
    
    deleted_employee = await emp_service.DeleteUserByIdService(id=id, db=db)
    return deleted_employee


@router.post("/employee/{emp_id}/department/{dept_id}", status_code=status.HTTP_200_OK)
async def AddEmployeeToDepartment(emp_id: int, dept_id : int, db : AsyncSession = Depends(get_db)):
    result = await emp_service.AddEmployeeToDepartmentService(emp_id=emp_id, dept_id=dept_id, db=db)
    return result



@router.delete("/employee/{emp_id}/department/{dept_id}", status_code=status.HTTP_200_OK)
async def DeleteEmployeeFromDepartment(emp_id: int, dept_id : int, db : AsyncSession = Depends(get_db)):
    result = await emp_service.DeleteEmployeeFromDepartmentService(emp_id=emp_id, dept_id=dept_id, db=db)
    return result


@router.post("/employee/{emp_id}/address", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponseAddress)
async def AddUserAddress(emp_id: int, body: AddressCreate, db: AsyncSession = Depends(get_db)):
    line1 = body.line1
    city = body.city
    postal_code = body.postal_code
    country = body.country
    address = {
        "line1": line1,
        "city": city,
        "postal_code": postal_code,
        "country": country
    }
    result = await emp_service.AddUserAddressService(emp_id=emp_id, address_data=address, db=db)
    return result

@router.put("/employee/{emp_id}/address", status_code = status.HTTP_200_OK, response_model=AddressResponse)
async def UpdateUserAddress(emp_id: int, address_id : int , body : AddressCreate, db : AsyncSession = Depends(get_db)):
    line1 = body.line1
    city = body.city
    postal_code = body.postal_code
    country = body.country
    address = {
        "line1": line1,
        "city": city,
        "postal_code": postal_code,
        "country": country
    }
    result = await emp_service.UpdateAddressService(emp_id=emp_id, address_data=address, address_id=address_id,db=db)
    return result


@router.delete("/employee/{emp_id}/address/{address_id}",status_code=200)
async def DeleteUserAddress(emp_id: int,address_id: int,db: AsyncSession = Depends(get_db)):
    return await emp_service.DeleteAddressService(emp_id=emp_id,address_id=address_id,db=db)




# @router.post("/login", status_code=status.HTTP_200_OK)
# async def LoginUserByEmail(body: dict = Body(...), db:AsyncSession = Depends(get_db)):
#     email = body.get("email")
#     password = body.get("password")

#     response = await emp_service.login(email=email, password=password, db=db)
#     return response