from sqlalchemy import Column, Integer, String, Date, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship

# Assuming Base is defined in session.py or a similar base file
# Adjust the import path if your Base is located elsewhere
from app.db.session import Base
from app.schemas.leave import LeaveStatus # Import the Enum from schema

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True) # Assuming 'employees' table name
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String, nullable=True)
    status = Column(SQLEnum(LeaveStatus), nullable=False, default=LeaveStatus.PENDING)

    # Define relationship back to Employee (optional but good practice)
    # Adjust 'Employee' class name and back_populates name if needed
    employee = relationship("Employee", back_populates="leave_requests")

    # Add __repr__ for easier debugging (optional)
    def __repr__(self):
        return f"<LeaveRequest(id={self.id}, employee_id={self.employee_id}, status='{self.status}')>"

# Ensure the related Employee model has the corresponding relationship defined:
# Example for app/db/models/employee.py:
# from sqlalchemy.orm import relationship
# class Employee(Base):
#     # ... other columns ...
#     leave_requests = relationship("LeaveRequest", back_populates="employee")