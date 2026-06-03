import pytest

from department.dept_repo import GetDepartmentByIdRepo
from exceptions.handlers import NotFoundException


@pytest.mark.asyncio
async def test_dept_by_id(db_session):
    with pytest.raises(NotFoundException) as exc_info:
        # `get_by_id` is `async def`, so we `await` it. The `await` lives
        # *inside* the `with` block — that's the call we expect to raise.
        await GetDepartmentByIdRepo(db=db_session, id=9999)

    # Step 2: details about the exception
    # `exc_info.value` is the actual exception object (a NotFoundException).
    # Our base `AppException` exposes `.detail` — we assert the missing ID
    # appears in it, locking in "this exception with this content", not just
    # "some NotFoundException was raised somewhere".
    assert "9999" in exc_info.value.detail
