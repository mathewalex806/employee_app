import pytest
from department.dept_repo import CreateDepartmentRepo


@pytest.mark.asyncio
async def test_create_dept(db_session):
    dept = await CreateDepartmentRepo(name="Test Department", db=db_session)

    assert dept.id == 1
    assert dept.name == "Test Department"
