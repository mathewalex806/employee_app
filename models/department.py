from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.entity import Entity
from sqlalchemy import ForeignKey
from models.employee import Employee


class Department(Entity):
    __tablename__ = "department"

    name : Mapped[str]=  mapped_column(String(255), nullable=False, unique=True)
