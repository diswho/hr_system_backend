from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated

# Import models and security functions from the new locations
from ..models.employee import Employee, EmployeeCreate
from ..models.user import UserInDB
from ..security import get_current_active_user, require_role

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    # dependencies=[Depends(get_current_active_user)], # Apply auth to all routes in this router
    responses={404: {"description": "Not found"}},
)

# --- Mock Employee Database (Should be moved to a data layer) ---
# TODO: Replace with actual database interaction
fake_employee_db: dict[int, Employee] = {}
next_employee_id: int = 1

# --- Employee Endpoints ---

# Requires 'manager' or 'admin' role
@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_role("manager"))])
async def create_employee(
    employee: EmployeeCreate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    """Creates a new employee."""
    global next_employee_id
    employee_id = next_employee_id
    # Create an Employee instance including the generated ID
    new_employee = Employee(id=employee_id, **employee.model_dump())
    fake_employee_db[employee_id] = new_employee
    next_employee_id += 1
    return new_employee

# Requires at least 'employee' role
@router.get("/", response_model=List[Employee],
            dependencies=[Depends(require_role("employee"))])
async def read_employees(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    """Retrieves a list of all employees."""
    return list(fake_employee_db.values())

# Requires at least 'employee' role
@router.get("/{employee_id}", response_model=Employee,
            dependencies=[Depends(require_role("employee"))])
async def read_employee(
    employee_id: int,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    """Retrieves a specific employee by their ID."""
    employee = fake_employee_db.get(employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee

# Requires 'manager' or 'admin' role
@router.put("/{employee_id}", response_model=Employee,
            dependencies=[Depends(require_role("manager"))])
async def update_employee(
    employee_id: int,
    employee_update: EmployeeCreate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    """Updates an existing employee's details."""
    if employee_id not in fake_employee_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    updated_employee = Employee(id=employee_id, **employee_update.model_dump())
    fake_employee_db[employee_id] = updated_employee
    return updated_employee

# Requires 'admin' role
@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_role("admin"))])
async def delete_employee(
    employee_id: int,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    """Deletes an employee by their ID."""
    if employee_id not in fake_employee_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    del fake_employee_db[employee_id]
    return None