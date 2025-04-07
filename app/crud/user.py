from sqlalchemy.orm import Session # Use SQLAlchemy Session type hint
from sqlmodel import select # Keep select from sqlmodel
from typing import List
from fastapi import HTTPException, status # Import HTTPException

from app.db.models.user import User
from app.db.models.user_role_link import UserRoleLink # Import link model
from app.schemas.user import UserCreate
from app import crud # Import crud module to access role CRUD
# Assume security functions exist for password hashing
from app.core.security import get_password_hash # Placeholder import

def get_user(db: Session, user_id: int) -> User | None:
    """Gets a single user by ID."""
    user = db.get(User, user_id)
    return user

def get_user_by_username(db: Session, username: str) -> User | None:
    """Gets a single user by username."""
    statement = select(User).where(User.username == username)
    result = db.execute(statement)
    user = result.scalars().first()
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Gets multiple users with pagination."""
    statement = select(User).offset(skip).limit(limit)
    result = db.execute(statement)
    users = result.scalars().all()
    return users

def create_user(db: Session, *, user_in: UserCreate) -> User:
    """Creates a new user and links roles if provided."""
    hashed_password = get_password_hash(user_in.password)
    # Exclude password and role_ids from the user object creation
    user_data = user_in.model_dump(exclude={"password", "role_ids"})
    db_user = User(**user_data, hashed_password=hashed_password)
    db.add(db_user)
    db.commit() # Commit user first to get an ID
    db.refresh(db_user)

    # Link roles if role_ids are provided
    if user_in.role_ids:
        for role_id in user_in.role_ids:
            role = crud.role.get_role(db, role_id=role_id)
            if not role:
                # Option 1: Raise error if a role ID is invalid
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Role with ID {role_id} not found.",
                )
                # Option 2: Silently ignore invalid role IDs (less strict)
                # continue
            link = UserRoleLink(user_id=db_user.id, role_id=role.id)
            db.add(link)
        db.commit() # Commit the links
        db.refresh(db_user) # Refresh again to load the relationships

    return db_user

# TODO: Implement update_user and delete_user functions
# def update_user(...)
# def delete_user(...)