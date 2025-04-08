from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session

from app import crud
from app.schemas.user import UserBase, UserCreate, UserUpdate # Import UserUpdate schema
from app.db.models.user import User  # Import the DB model for response_model if needed, or use schema
from app.db.session import get_db  # Dependency for DB session
from app.core.security import require_role  # Import the role checker dependency

router = APIRouter(
    dependencies=[Depends(require_role("system"))]  # Apply role check to all user endpoints
)

# system


@router.post("/", response_model=UserBase, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
):
    """
    Create new user.
    """
    user = crud.user.get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    # Add email check if email should be unique
    # user_by_email = crud.user.get_user_by_email(db, email=user_in.email)
    # if user_by_email:
    #     raise HTTPException(...)

    user = crud.user.create_user(db=db, user_in=user_in)
    return user


@router.get("/", response_model=List[UserBase])
def read_users_endpoint(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve users.
    """
    # Filter users by the "system" role
    # users = crud.user.get_users(db, skip=skip, limit=limit, role_name="system")
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserBase)
def read_user_by_id_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Get user by ID.
    """
    user = crud.user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this ID does not exist in the system",
        )
    return user

@router.put("/{user_id}", response_model=UserBase)
def update_user_endpoint(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
):
    """
    Update a user.
    """
    user = crud.user.get_user(db, user_id=user_id) # Check if user exists first
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this ID does not exist in the system",
        )
    updated_user = crud.user.update_user(db=db, user_id=user_id, user_in=user_in)
    return updated_user


@router.delete("/{user_id}", response_model=UserBase) # Or use status_code=204 and no response_model
def delete_user_endpoint(
    *,
    db: Session = Depends(get_db),
    user_id: int,
):
    """
    Delete a user.
    """
    user = crud.user.get_user(db, user_id=user_id) # Check if user exists first
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this ID does not exist in the system",
        )
    deleted_user = crud.user.delete_user(db=db, user_id=user_id)
    return deleted_user # Return the deleted user object
