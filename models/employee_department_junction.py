from models import Employee, Department
from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from models.entity import Entity


class EmployeeDepartmentJunction(Entity):
    __tablename__ = "employee_department"
    __table_args__ = (
    UniqueConstraint(
        "employee_id",
        "department_id",
        name="uq_employee_department",
    ),
)

    employee_id : Mapped[int] = mapped_column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True ) 
    department_id : Mapped[int] = mapped_column(Integer, ForeignKey("department.id", ondelete="CASCADE"), nullable=False, index=True)

