import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from database import Base
from employee import employee_service as employee_service
from employee.schemas import EmployeeCreate


@pytest.mark.asyncio
async def test_create_employee_persists_the_record():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession)

    async with session_factory() as db:
        body = EmployeeCreate(
            name="Ada", email="ada@example.com", password="secret123", age=50
        )
        # employee = await db.run_sync(
        #     lambda sync_session: employee_service.create(sync_session, name= body.name, email= body.email, password = body.password)
        # )
        employee = await employee_service.create(
            db=db,
            name=body.name,
            email=body.email,
            password=body.password,
        )

        assert employee.id is not None
        assert employee.name == "Ada"
        assert employee.email == "ada@example.com"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
