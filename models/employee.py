"""
Employee entity — ORM mapped class for table `employees`.
Register all new models in env.py file
"""

from datetime import datetime
from typing import Any

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.address import Address
from models.entity import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.department import Department

import enum
from sqlalchemy import Enum


def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


class EmployeeRole(str, enum.Enum):
    UI = "UI"
    UX = "UX"
    DEVELOPER = "Developer"
    HR = "HR"


class Status(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    PROBATION = "Probation"


class Employee(Entity):
    __tablename__ = "employees"
    __abstract__ = False

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[Status] = mapped_column(
        Enum(
            Status,
            name="employeestatus",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=True,
    )

    experience: Mapped[str] = mapped_column(String(10), nullable=True)

    role: Mapped[EmployeeRole] = mapped_column(
        Enum(
            EmployeeRole,
            name="employeerole",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        server_default=EmployeeRole.DEVELOPER.value,
    )
    addresses: Mapped[list["Address"]] = relationship(
        "Address",
        back_populates="employee",
        lazy="selectin",
    )
    departments: Mapped[list["Department"]] = relationship(
        "Department",
        secondary="employee_department",
        back_populates="employees",
        lazy="selectin",
    )

    def to_api_dict(self) -> dict[str, Any]:
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": _datetime_to_iso(self.created_at),
            "updated_at": _datetime_to_iso(self.updated_at),
            "deleted_at": _datetime_to_iso(self.deleted_at),
        }
