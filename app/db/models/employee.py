from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

# Assuming Base is defined in session.py or a similar base file
from app.db.session import Base
# Import User model if needed for relationships (e.g., employee linked to a user account)
# from .user import User # Example

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    hire_date = Column(Date, nullable=False)
    job_title = Column(String(100), nullable=False)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    salary = Column(Float, nullable=True)
    
    # Relationships
    position = relationship("Position")
    department = relationship("Department")

    # Optional: Link to a user account if applicable
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Example
    # user = relationship("User", back_populates="employee_profile") # Example

    # Relationship to LeaveRequest
    # The 'LeaveRequest' model should have `employee = relationship("Employee", back_populates="leave_requests")`
    leave_requests = relationship("LeaveRequest", back_populates="employee", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.first_name} {self.last_name}')>"

# Ensure the related User model (if used) has the corresponding relationship:
# Example for app/db/models/user.py:
# from sqlalchemy.orm import relationship
# class User(Base):
#     # ... other columns ...
#     employee_profile = relationship("Employee", back_populates="user", uselist=False) # Example for one-to-one