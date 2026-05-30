from pydantic import BaseModel
from pydantic.v1 import ConfigDict


class DepartmentBase(BaseModel):
    name: str

class DepartmentResponse(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name : str
    