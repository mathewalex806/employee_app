from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.entity import Entity
from models.employee import Employee


class Department(Entity):
    __tablename__ = "department"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    employees: Mapped[list["Employee"]] = relationship(
        "Employee",
        secondary="employee_department",
        back_populates="departments",
    )
