from datetime import date
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

# Forward references for relationships
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .position import Position
    from .department import Department
    from .leave import LeaveRequest
    from .user import User


class Employee(SQLModel, table=True):
    __tablename__ = "employees"

    id: int | None = Field(default=None, primary_key=True, index=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(unique=True, index=True)
    phone: str | None = Field(default=None, max_length=20)
    hire_date: date
    job_title: str = Field(max_length=100)
    salary: float | None = Field(default=None)

    # Foreign Keys
    position_id: int | None = Field(default=None, foreign_key="positions.id", index=True)
    department_id: int | None = Field(default=None, foreign_key="departments.id", index=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True, nullable=True) # Foreign key to User

    # Relationships
    position: Optional["Position"] = Relationship(back_populates="employees") # Assuming 'employees' in Position model
    department: Optional["Department"] = Relationship(back_populates="employees") # Assuming 'employees' in Department model
    leave_requests: List["LeaveRequest"] = Relationship(back_populates="employee")
    user: Optional["User"] = Relationship(back_populates="employee_profile") # Link back to User

    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.first_name} {self.last_name}')>"

# Notes for related models (ensure they are also SQLModel and have correct back_populates):
# In app/db/models/position.py:
# class Position(SQLModel, table=True):
#     # ... other fields
#     employees: List["Employee"] = Relationship(back_populates="position")

# In app/db/models/department.py:
# class Department(SQLModel, table=True):
#     # ... other fields
#     employees: List["Employee"] = Relationship(back_populates="department")

# In app/db/models/leave.py:
# class LeaveRequest(SQLModel, table=True):
#     # ... other fields
#     employee_id: Optional[int] = Field(default=None, foreign_key="employees.id")
#     employee: Optional["Employee"] = Relationship(back_populates="leave_requests")

# In app/db/models/user.py (if used):
# class User(SQLModel, table=True):
#     # ... other fields
#     employee_profile: Optional["Employee"] = Relationship(back_populates="user") # One-to-one if uselist=False was intended
