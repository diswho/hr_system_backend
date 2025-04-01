from pydantic import BaseModel, Field
from typing import Optional, List

# Base schema with shared fields
class DepartmentBase(BaseModel):
    name: str = Field(..., max_length=50, example="Engineering")
    description: Optional[str] = Field(None, max_length=255, example="Software development department")

# Schema for creating new departments
class DepartmentCreate(DepartmentBase):
    pass

# Schema for updating departments
class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=255)

# Full department schema - returned by API
class Department(DepartmentBase):
    id: int

    class Config:
        from_attributes = True