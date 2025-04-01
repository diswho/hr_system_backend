from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional

# Enum for Leave Status
class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

# Base schema with common attributes
class LeaveRequestBase(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = None

# Schema for creating a leave request (input)
class LeaveRequestCreate(LeaveRequestBase):
    pass # Status will default to PENDING upon creation

# Schema for reading/representing a leave request (output)
class LeaveRequest(LeaveRequestBase):
    id: int
    status: LeaveStatus = LeaveStatus.PENDING # Default status

    class Config:
        from_attributes = True # For ORM mode compatibility if needed later