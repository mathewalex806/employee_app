from fastapi import FastAPI
from dataclasses import dataclass
from typing import TypedDict
from middleware.logging import RequestLoggingMiddleware
import logging
from fastapi.middleware.cors import CORSMiddleware
from database.connection import create_tables, get_db
from contextlib import asynccontextmanager
from fastapi import Body
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi import HTTPException, status

from sqlalchemy import select
from employee import router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await create_tables()
    yield



app = FastAPI(
    title="Employee CRUD Application",
    description="Simple Employee management software",
    version="1.0.0",
    # lifespan=lifespan
)

# app.add_middleware(RequestLoggingMiddleware)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=False,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["X-Process-Time"],
# )

app.include_router(router)



# class EmployeeRegisteration(TypedDict):
#     name : str
#     username : str
#     password : str



# class StoredUser(TypedDict):
#     id : int
#     name : str
#     username : str
#     designation : str
#     salary : float
#     is_deleted : bool

# class AllUsers(TypedDict):
#     users : dict[int, StoredUser]


# _app_dict = {}
# _counter = 0

# @app.get("/", status_code=200)
# def base_endpoint():
#     return {"message":"base endpoint"}


# @app.post("/employee", status_code=status.HTTP_201_CREATED, tags=["Employees"])
# async def create_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
#     name = body.get("name")
#     email = body.get("email")
#     if not isinstance(name, str) or not name.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
#     if not isinstance(email, str) or not email.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
#     db_employee = Employee(name=name.strip(), email=email.strip())
#     db.add(db_employee)
#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
#     await db.refresh(db_employee)
#     return db_employee.to_api_dict()

# @app.post("/register", status_code=201, )
# async def register(body : dict = Body(...), db:AsyncSession = Depends(get_db)):
    
#     return db_employee.to_api_dict()

    


# @app.get("/users", status_code=200)
# async def GetAllEmployee(db:AsyncSession = Depends(get_db)):
#     query = select(Employee).where(Employee.deleted_at.is_(None))
#     result = await db.scalars(query)
#     return [r.to_api_dict() for r in result.all()]


# @app.get("/user/{id}", status_code=200)
# async def getUserById( id:int, db:AsyncSession= Depends(get_db)):
#     if id is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#     query = select(Employee).where(Employee.id == id)
#     result = await db.scalars(query)
#     employee = result.first()
#     if not employee:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return employee.to_api_dict()


# @app.delete("/user/{id}", status_code=200)
# async def deleteUserById(id:int, db:AsyncSession= Depends(get_db)):
#     if id is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
#     query = select(Employee).where(Employee.id == id)
#     result = await db.scalars(query)
#     employee = result.first()
#     if employee is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    
#     try:
#         await db.delete(employee)
#         await db.commit()
#     except Exception as e:
#         print(e)
#         await db.rollback()

#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

#     return {"message":"Record Deleted"}







# @app.put("/users/{id}")
# async def update(id:int , body : dict=Body(...),db:AsyncSession= Depends(get_db)):
#     if id is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
#     query = select(Employee).where(Employee.id == id)
#     result = await db.scalars(query)
#     employee = result.first()
#     if employee is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         name = body.get("name")
#         email = body.get("email")
#         employee.name = name
#         employee.email = email

#         await db.commit()
#     except Exception as e:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
#     return employee





def main():
    print("Hello from employee-app!")


if __name__ == "__main__":
    main()
