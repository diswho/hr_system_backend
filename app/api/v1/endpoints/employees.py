from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated
from sqlalchemy.orm import Session # Import Session

# Import schemas, security, CRUD, DB dependency, and Employee schema for response
from app.schemas.employee import Employee, EmployeeCreate, EmployeeUpdate # Import Employee and EmployeeUpdate
from app.schemas.user import UserInDB
from app.core.security import get_current_active_user, require_role
from app.crud import crud_employee # Import employee CRUD functions
from app.db.session import get_db # Import DB session dependency

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    # dependencies=[Depends(get_current_active_user)], # Apply auth to all routes in this router
    responses={404: {"description": "Not found"}},
)

# --- (Mock database removed) ---

# --- Employee Endpoints ---

# Requires 'manager' or 'admin' role
@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_role("manager"))])
async def create_employee(
    employee: EmployeeCreate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: Session = Depends(get_db) # Add DB session dependency
):
    """Creates a new employee in the database."""
    # Check if employee already exists
    db_employee = crud_employee.get_employee_by_email(db, email=employee.email)
    if db_employee:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    # Create employee using CRUD function
    return crud_employee.create_employee(db=db, employee=employee)

# Requires at least 'employee' role
@router.get("/", response_model=List[Employee],
            dependencies=[Depends(require_role("employee"))])
async def read_employees(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    skip: int = 0, # Add pagination
    limit: int = 100,
    db: Session = Depends(get_db) # Add DB session dependency
):
    """Retrieves a list of all employees."""
    employees = crud_employee.get_employees(db, skip=skip, limit=limit)
    return employees

# Requires at least 'employee' role
@router.get("/{employee_id}", response_model=Employee,
            dependencies=[Depends(require_role("employee"))])
async def read_employee(
    employee_id: int,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: Session = Depends(get_db) # Add DB session dependency
):
    """Retrieves a specific employee by their ID."""
    db_employee = crud_employee.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return db_employee

# Requires 'manager' or 'admin' role
@router.put("/{employee_id}", response_model=Employee,
            dependencies=[Depends(require_role("manager"))])
async def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate, # Use EmployeeUpdate schema
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: Session = Depends(get_db) # Add DB session dependency
):
    """Updates an existing employee's details."""
    # Use CRUD function to update
    db_employee = crud_employee.update_employee(db=db, employee_id=employee_id, employee_update=employee_update)
    if db_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    # Check for email conflict if email is being updated
    if employee_update.email:
        existing_employee = crud_employee.get_employee_by_email(db, email=employee_update.email)
        if existing_employee and existing_employee.id != employee_id:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered by another employee")
    # Re-fetch the updated employee to ensure data consistency before returning
    # (Alternatively, the update_employee CRUD could return the updated object directly if refreshed)
    updated_employee = crud_employee.get_employee(db, employee_id=employee_id)
    return updated_employee

# Requires 'admin' role
@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_role("admin"))])
async def delete_employee(
    employee_id: int,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: Session = Depends(get_db) # Add DB session dependency
):
    """Deletes an employee by their ID."""
    # Use CRUD function to delete
    deleted_employee = crud_employee.delete_employee(db=db, employee_id=employee_id)
    if deleted_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    # Return None with 204 status code (already set in decorator)
    return None