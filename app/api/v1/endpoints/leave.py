from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated
from sqlalchemy.orm import Session # Import Session

# Import schemas, security functions, CRUD, and DB dependency
from app.schemas.leave import LeaveRequest, LeaveRequestCreate, LeaveStatus
from app.schemas.user import UserInDB
from app.core.security import get_current_active_user, require_role
from app.crud import crud_leave # Import leave CRUD functions
from app.db.session import get_db # Import DB session dependency (adjust path if needed)

router = APIRouter(
    prefix="/leave",
    tags=["leave"],
    responses={404: {"description": "Not found"}},
)

# --- (Mock database removed) ---

# --- Leave Request Endpoints ---

# Requires at least 'employee' role to create a request
@router.post("/", response_model=LeaveRequest, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_role("employee"))])
async def create_leave_request(
    leave_request: LeaveRequestCreate,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: Session = Depends(get_db) # Moved DB session dependency to the end
):
    """Creates a new leave request in the database."""
    # Removed global ID logic

    # Basic validation: Ensure end_date is not before start_date
    if leave_request.end_date < leave_request.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date cannot be before start date."
        )

    # TODO: Add logic to check if leave_request.employee_id exists (e.g., using crud_employee.get_employee)
    # TODO: Add logic for managers/admins creating requests for others (e.g., checking roles and allowing different employee_id)
    # For now, assume the employee_id in the request is valid and intended

    # Create request using CRUD function
    db_leave_request = crud_leave.create_leave_request(db=db, leave_request=leave_request)
    return db_leave_request

# Requires 'manager' or 'admin' role to view all requests
@router.get("/", response_model=List[LeaveRequest],
            dependencies=[Depends(require_role("manager"))])
async def read_all_leave_requests(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db) # Moved DB session dependency to the end
):
    """Retrieves a list of all leave requests (manager/admin access)."""
    # Retrieve requests using CRUD function
    leave_requests = crud_leave.get_leave_requests(db=db, skip=skip, limit=limit)
    return leave_requests

# Requires at least 'employee' role to view a specific request
# TODO: Add logic to ensure employees can only view their own requests unless manager/admin
@router.get("/{request_id}", response_model=LeaveRequest,
            dependencies=[Depends(require_role("employee"))])
async def read_leave_request(
    request_id: int,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: Session = Depends(get_db) # Moved DB session dependency to the end
):
    """Retrieves a specific leave request by its ID."""
    # Retrieve request using CRUD function
    db_request = crud_leave.get_leave_request(db=db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave request not found")

    # Implement access control
    is_owner = db_request.employee_id == current_user.id
    is_manager_or_admin = any(role.name in ["manager", "admin"] for role in current_user.roles)

    if not is_owner and not is_manager_or_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this request")

    return db_request

# TODO: Add endpoints for updating status (PUT /leave/{request_id}/status) - requires manager/admin
# TODO: Add endpoint for deleting requests (DELETE /leave/{request_id}) - requires admin?