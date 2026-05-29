from pydantic import BaseModel, ConfigDict, Field, field_validator


class AddressCreate(BaseModel):
    line1 : str
    city : str
    postal_code : int 
    country : str

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls,v : str):
        if not v.isdigit():
            raise ValueError("Postal code is incorrect")


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    name: str = Field(min_length=1)
    email : str
    age : int | None = Field(ge=0, lt=150)
    address : AddressCreate | None