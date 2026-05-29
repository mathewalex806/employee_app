"""
Employee Router
"""


from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import create_tables, get_db
from fastapi import Depends
from fastapi import HTTPException, status

from fastapi import APIRouter, Body
import employee.employee_service as emp_service
from employee.schemas import EmployeeCreate, AddressCreate, EmployeeResponse, EmployeeResponseByUserId

router = APIRouter(prefix="/api/v1", tags=["Employee"])

@router.post("/employee", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
async def create_employee(body: EmployeeCreate, db:AsyncSession = Depends(get_db)):
    name = body.name
    email = body.email

    employee =  await emp_service.create(db=db, name=name, email=email)
    return employee


@router.get("/users", status_code=status.HTTP_200_OK, response_model= list[EmployeeResponse])
async def GetUsers(db:AsyncSession = Depends(get_db)):
    name = "Alex"
    print(f"{name}")
    employees = await emp_service.GetAllUsers(db=db)
    return employees

@router.get("/user/{id}", status_code=status.HTTP_200_OK, response_model= EmployeeResponseByUserId)
async def GetUserById(id:int, db:AsyncSession = Depends(get_db)):
    employee = await emp_service.GetUserById(id=id, db=db)
    return employee


@router.put("/user/{id}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse)
async def UpdateUserById(id:int, body  : dict = Body(...), db:AsyncSession = Depends(get_db)):
    name = body.get("name")
    email = body.get("email")

    updated_employee = await emp_service.UpdateUserByIdService(db=db, name=name, email=email, id=id)
    return updated_employee


@router.delete("/user/{id}", status_code=status.HTTP_200_OK)
async def DeleteUserById(id:int, db:AsyncSession = Depends(get_db)):
    
    deleted_employee = await emp_service.DeleteUserByIdService(id=id, db=db)
    return deleted_employee