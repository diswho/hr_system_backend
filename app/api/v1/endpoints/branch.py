from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session

from app import crud, schemas
from app.db import session # Assuming session dependency setup
from app.db.models.branch import Branch # Import the model for response_model

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Branch, status_code=status.HTTP_201_CREATED)
def create_branch(
    *,
    db: Session = Depends(get_db),
    branch_in: schemas.BranchCreate,
    # Add dependency for current user/permissions if needed
    # current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    Create a new branch.
    """
    branch = crud.crud_branch.get_branch_by_name(db, name=branch_in.name)
    if branch:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A branch with this name already exists.",
        )
    new_branch = crud.crud_branch.create_branch(db=db, branch=branch_in)
    return new_branch

@router.get("/", response_model=List[schemas.Branch])
def read_branches(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # Add dependency for current user/permissions if needed
    # current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve branches.
    """
    branches = crud.crud_branch.get_branches(db, skip=skip, limit=limit)
    return branches

@router.get("/{branch_id}", response_model=schemas.Branch)
def read_branch(
    *,
    db: Session = Depends(get_db),
    branch_id: int,
    # Add dependency for current user/permissions if needed
    # current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get branch by ID.
    """
    branch = crud.crud_branch.get_branch(db, branch_id=branch_id)
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    return branch

@router.put("/{branch_id}", response_model=schemas.Branch)
def update_branch(
    *,
    db: Session = Depends(get_db),
    branch_id: int,
    branch_in: schemas.BranchUpdate,
    # Add dependency for current user/permissions if needed
    # current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    Update a branch.
    """
    branch = crud.crud_branch.get_branch(db, branch_id=branch_id)
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    # Check for name conflict if name is being updated
    if branch_in.name:
        existing_branch = crud.crud_branch.get_branch_by_name(db, name=branch_in.name)
        if existing_branch and existing_branch.id != branch_id:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Branch name already in use")
    updated_branch = crud.crud_branch.update_branch(db=db, db_branch=branch, branch_in=branch_in)
    return updated_branch

@router.delete("/{branch_id}", response_model=schemas.Branch) # Or return status code/message
def delete_branch(
    *,
    db: Session = Depends(get_db),
    branch_id: int,
    # Add dependency for current user/permissions if needed
    # current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    Delete a branch.
    """
    branch = crud.crud_branch.get_branch(db, branch_id=branch_id)
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    # Add checks here if deleting a branch with associated users/employees is restricted
    deleted_branch = crud.crud_branch.delete_branch(db=db, branch_id=branch_id)
    return deleted_branch # Or return {"message": "Branch deleted successfully"}