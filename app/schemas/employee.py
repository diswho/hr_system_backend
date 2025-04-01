from pydantic import BaseModel, EmailStr
from typing import Optional

# Base schema with common attributes
class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    position: Optional[str] = None
    department: Optional[str] = None

# Schema for creating an employee (inherits from Base)
# No 'id' here as it's generated upon creation
class EmployeeCreate(EmployeeBase):
    pass

# Schema for reading/representing an employee (inherits from Base)
# Includes the 'id'
class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True # For ORM mode compatibility if needed later