from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr, model_validator


class AddressCreate(BaseModel):
    line1 : str
    city : str
    postal_code : str 
    country : str

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls,v : str):
        if not v.isdigit():
            raise ValueError("Postal code is incorrect")
        return v
        
    @model_validator(mode="after")
    def validate_postal_based_on_country(self):
        country = self.country.strip().upper()
        if country in ("USA", "US") and len(self.postal_code) != 5:
            raise ValueError("US Postal code length is 5")
        elif country in ("IN") and len(self.postal_code) !=6:
            raise ValueError("Indian postal code length is 6")
        
        return self

class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    name: str = Field(min_length=1)
    email : EmailStr
    age : int | None = Field(ge=0, lt=150)
    address : AddressCreate | None
    password : str = Field(min_length=6)


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int 
    name : str
    email : EmailStr
    age : int | None

class EmployeeResponseByUserId(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int 
    name : str
    email : EmailStr
    age : int | None
    created_at : datetime
    updated_at : datetime | None
    deleted_at : datetime | None