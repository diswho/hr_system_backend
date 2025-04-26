from pydantic import BaseModel, EmailStr, Field, ConfigDict # <-- Import ConfigDict
from typing import Optional, List, Union
from datetime import date
from app.schemas.position import Position, PositionCreate
from app.schemas.department import Department, DepartmentCreate
from app.schemas.branch import Branch, BranchCreate # <-- Import Branch schemas

# Base schema with common attributes
class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    job_title: str # Added required field
    hire_date: date # Added required field
    position: Optional[Union[Position, PositionCreate]] = None
    department: Optional[Union[Department, DepartmentCreate]] = None

    branch_id: Optional[int] = None # <-- Add branch_id
    branch: Optional[Union[Branch, BranchCreate]] = None # <-- Add nested branch

# Schema for creating an employee (inherits from Base)
# No 'id' here as it's generated upon creation
class EmployeeCreate(EmployeeBase):
    branch_id: Optional[int] = None # <-- Add branch_id for creation

# Schema for updating an employee (all fields optional)
class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    job_title: Optional[str] = None
    hire_date: Optional[date] = None
    position: Optional[str] = None
    department: Optional[str] = None
    # Note: phone_number and salary were missing from EmployeeBase, add them here if needed for update
    phone_number: Optional[str] = None # Added based on model
    salary: Optional[float] = None # Added based on model

    branch_id: Optional[int] = None # <-- Add branch_id for update

# Schema for reading/representing an employee (inherits from Base)
# Includes the 'id'
class Employee(EmployeeBase):
    id: int

    # Use model_config for Pydantic v2
    model_config = ConfigDict(from_attributes=True)