from pydantic import BaseModel, ConfigDict, Field


class AddressCreate(BaseModel):
    line1 : str
    city : str
    postal_code : int 
    country : str


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    name: str = Field(min_length=1)
    email : str
    age : int | None = Field(ge=0, lt=150)
    address : AddressCreate | None