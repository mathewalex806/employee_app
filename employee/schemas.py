from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    EmailStr,
    model_validator,
)

from models.employee import EmployeeRole, Status


class AddressCreate(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v: str):
        if not v.isdigit():
            raise ValueError("Postal code is incorrect")
        return v

    @model_validator(mode="after")
    def validate_postal_based_on_country(self):
        country = self.country.strip().upper()
        if country in ("USA", "US") and len(self.postal_code) != 5:
            raise ValueError("US Postal code length is 5")
        elif country in ("IN") and len(self.postal_code) != 6:
            raise ValueError("Indian postal code length is 6")

        return self


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1)
    email: EmailStr
    age: int | None = Field(ge=0, lt=150)
    address: AddressCreate | None = None
    password: str = Field(min_length=6)
    role: EmployeeRole | None = None
    status: Status | None = None
    experience: str = Field(min_length=1)


class EmployeeResponseByUserId(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    role: str
    age: int | None
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None


class AddressResponse(BaseModel):
    id: int
    line_1: str | None
    city: str | None
    postal_code: int | None
    country: str | None

    model_config = ConfigDict(from_attributes=True)


class DepartmentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class EmployeeResponseAddress(BaseModel):
    id: int
    name: str
    email: str
    role: str
    addresses: list[AddressResponse]
    departments: list[DepartmentSchema]
    created_at: datetime | None
    experience: str | None
    status: Status | None
    model_config = ConfigDict(from_attributes=True)


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    age: int | None
    role: EmployeeRole | None = None
    address: AddressResponse | None = None


class UpdateEmployeeDetailsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    age: int | None
    status: Status
    experience: str
    role: EmployeeRole | None = None


class UpdateEmployeeDetailsRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: EmailStr
    age: int | None
    experience: str | None
    status: Status | None = None
    role: EmployeeRole | None = None


class AddEmployeeToDepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    age: int | None
    role: EmployeeRole | None = None
    departments: list[DepartmentSchema]


class GetAllUsersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    age: int | None
    role: EmployeeRole | None = None
    departments: list[DepartmentSchema]
    addresses: list[AddressCreate]
    experience: str
    status: str
