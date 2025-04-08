from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session

from app import crud
from app.schemas.role import RoleRead, RoleCreate
from app.db.session import get_db # Correct import for DB session
from app.core.security import require_role # Import the role checker dependency

router = APIRouter(
    dependencies=[Depends(require_role("system"))] # Apply role check to all role endpoints
)

@router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role_endpoint(
    *,
    db: Session = Depends(get_db),
    role_in: RoleCreate
):
    """
    Create new role.
    """
    role = crud.role.get_role_by_name(db, name=role_in.name)
    if role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A role with this name already exists.",
        )
    role = crud.role.create_role(db=db, role_in=role_in)
    return role

@router.get("/", response_model=List[RoleRead])
def read_roles_endpoint(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve roles.
    """
    roles = crud.role.get_roles(db, skip=skip, limit=limit)
    return roles

@router.get("/{role_id}", response_model=RoleRead)
def read_role_by_id_endpoint(
    role_id: int,
    db: Session = Depends(get_db),
):
    """
    Get role by ID.
    """
    role = crud.role.get_role(db, role_id=role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    return role

# TODO: Add endpoints for updating and deleting roles if needed
# @router.put("/{role_id}", ...)
# @router.delete("/{role_id}", ...)