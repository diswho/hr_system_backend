from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date

class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=20)
    hire_date: date
    job_title: str = Field(..., max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    salary: Optional[float] = Field(None, gt=0)

class EmployeeCreate(EmployeeBase):
    pass # No extra fields needed for creation initially

class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True # Use Pydantic V2 standard

# Note: The fake DB variables (fake_employee_db, next_employee_id)
# will be moved to the employee router later where they are used.