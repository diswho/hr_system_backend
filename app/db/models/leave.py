from datetime import date

from sqlmodel import Field, Relationship, SQLModel

from app.schemas.leave import LeaveStatus # Import the Enum from schema

# Forward references for relationships
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .employee import Employee


class LeaveRequest(SQLModel, table=True):
    __tablename__ = "leave_requests"

    id: int | None = Field(default=None, primary_key=True, index=True)
    start_date: date
    end_date: date
    reason: str | None = Field(default=None)
    status: LeaveStatus = Field(default=LeaveStatus.PENDING)

    # Foreign Key
    employee_id: int = Field(foreign_key="employees.id", index=True)

    # Relationship back to Employee
    employee: "Employee" = Relationship(back_populates="leave_requests")

    def __repr__(self):
        return f"<LeaveRequest(id={self.id}, employee_id={self.employee_id}, status='{self.status}')>"

# Ensure the related Employee model (app/db/models/employee.py) has:
# from typing import List
# ...
# class Employee(SQLModel, table=True):
#     # ... other fields
#     leave_requests: List["LeaveRequest"] = Relationship(back_populates="employee")