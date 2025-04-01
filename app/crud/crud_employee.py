from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.db.models.employee import Employee
from app.db.models.position import Position
from app.db.models.department import Department
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.schemas.position import Position
from app.schemas.department import Department

def get_employee(db: Session, employee_id: int) -> Optional[Employee]:
    """
    Retrieves a single employee by their ID.
    """
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_employee_by_email(db: Session, email: str) -> Optional[Employee]:
    """
    Retrieves a single employee by their email address.
    """
    return db.query(Employee).filter(Employee.email == email).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100) -> List[Employee]:
    """
    Retrieves a list of employees with pagination.
    """
    return db.query(Employee).offset(skip).limit(limit).all()

def create_employee(db: Session, employee: EmployeeCreate) -> Employee:
    """
    Creates a new employee in the database with position and department.
    """
    employee_data = employee.model_dump(exclude={"position", "department"})
    
    # Handle position if provided
    position = None
    if employee.position:
        if isinstance(employee.position, int):
            position = db.query(Position).get(employee.position)
        else:
            position = db.query(Position).filter_by(name=employee.position.name).first()
            if not position:
                position = Position(**employee.position.model_dump())
                db.add(position)
                db.commit()
                db.refresh(position)
    
    # Handle department if provided
    department = None
    if employee.department:
        if isinstance(employee.department, int):
            department = db.query(Department).get(employee.department)
        else:
            department = db.query(Department).filter_by(name=employee.department.name).first()
            if not department:
                department = Department(**employee.department.model_dump())
                db.add(department)
                db.commit()
                db.refresh(department)
    
    # Create employee with relationships
    db_employee = Employee(
        **employee_data,
        position=position,
        department=department
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee_update: EmployeeUpdate) -> Optional[Employee]:
    """
    Updates an existing employee including position and department relationships.
    """
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return None

    update_data = employee_update.model_dump(exclude={"position", "department"}, exclude_unset=True)
    
    # Handle position update if provided
    if employee_update.position is not None:
        if isinstance(employee_update.position, int):
            position = db.query(Position).get(employee_update.position)
        elif isinstance(employee_update.position, dict):
            position = db.query(Position).filter_by(name=employee_update.position["name"]).first()
            if not position:
                position = Position(**employee_update.position)
                db.add(position)
                db.commit()
                db.refresh(position)
        else:
            position = None
        update_data["position"] = position
    
    # Handle department update if provided
    if employee_update.department is not None:
        if isinstance(employee_update.department, int):
            department = db.query(Department).get(employee_update.department)
        elif isinstance(employee_update.department, dict):
            department = db.query(Department).filter_by(name=employee_update.department["name"]).first()
            if not department:
                department = Department(**employee_update.department)
                db.add(department)
                db.commit()
                db.refresh(department)
        else:
            department = None
        update_data["department"] = department
    
    # Apply all updates
    for key, value in update_data.items():
        setattr(db_employee, key, value)
    
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int) -> Optional[Employee]:
    """
    Deletes an employee from the database.
    """
    db_employee = get_employee(db, employee_id)
    if not db_employee:
        return None
    db.delete(db_employee)
    db.commit()
    return db_employee