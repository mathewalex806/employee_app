from fastapi import APIRouter, Depends
from department.schemas import DepartmentBase, DepartmentResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from department.dept_service import CreateDepartmentService, GetDepartmentByIdService, GetAllDepartments, UpdateDepartmentByIdService, DeleteDepartmentByIdService       
dept_router = APIRouter(prefix = "/departments", tags=["Departments"])


@dept_router.post("/create", status_code=201, response_model=DepartmentResponse) 
async def create_department(body : DepartmentBase, db:AsyncSession = Depends(get_db)):
    name = body.name
    return await CreateDepartmentService(db=db, name=name)



@dept_router.get("/get/{id}", status_code=200, response_model=DepartmentResponse)
async def get_department(id: int, db:AsyncSession = Depends(get_db)):
    return await GetDepartmentByIdService(id=id, db=db)

@dept_router.get("/get-all", status_code=200, response_model=list[DepartmentResponse])
async def get_all_departments(db:AsyncSession = Depends(get_db)):
    return await GetAllDepartments(db=db)

@dept_router.put("/update/{id}", status_code=200, response_model=DepartmentResponse)
async def update_department(id: int, body: DepartmentBase, db:AsyncSession = Depends(get_db)):
    name = body.name
    return await UpdateDepartmentByIdService(id=id, name=name, db=db)

@dept_router.delete("/delete/{id}", status_code=204)
async def delete_department(id: int, db:AsyncSession = Depends(get_db)):
    return await DeleteDepartmentByIdService(id=id, db=db)
