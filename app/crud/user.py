from sqlalchemy.orm import Session, joinedload  # Use SQLAlchemy Session type hint, Import joinedload
from sqlmodel import select  # Keep select from sqlmodel
from typing import List
from fastapi import HTTPException, status  # Import HTTPException

from app.db.models.user import User
from app.db.models.user_role_link import UserRoleLink  # Import link model
from app.db.models.role import Role  # Import Role model for joinedload path
from app.schemas.user import UserCreate, UserUpdate  # Import UserUpdate
from app import crud  # Import crud module to access role CRUD
from app.core.hashing import get_password_hash  # Import from new hashing module
# Assume security functions exist for password hashing
# from app.core.security import get_password_hash # Removed import from security


def get_user(db: Session, user_id: int) -> User | None:
    """Gets a single user by ID."""
    user = db.get(User, user_id)
    return user


def get_user_by_username(db: Session, username: str) -> User | None:
    """Gets a single user by username, eagerly loading roles."""
    statement = (
        select(User)
        .where(User.username == username)
        # Eagerly load roles through the link table
        # .options(joinedload(User.role_links).joinedload(UserRoleLink.role))
    )
    result = db.execute(statement)
    # Use unique().scalars().first() to handle potential duplicate User rows from joins
    user = result.unique().scalars().first()
    return user


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    role_name: str | None = None  # Add optional role_name filter
) -> List[User]:
    """Gets multiple users with pagination, optionally filtering by role name."""
    statement = select(User).distinct()  # Select distinct users

    if role_name:
        # Join through the link table to filter by Role name
        statement = (
            statement
            .join(User.role_links)  # User -> UserRoleLink relationship
            .join(UserRoleLink.role)  # UserRoleLink -> Role relationship
            .where(Role.name == role_name)  # Filter on Role.name
        )

    statement = statement.offset(skip).limit(limit)  # Apply pagination

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
    db.commit()  # Commit user first to get an ID
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
        db.commit()  # Commit the links
        db.refresh(db_user)  # Refresh again to load the relationships

    return db_user


def update_user(db: Session, *, user_id: int, user_in: UserUpdate) -> User | None:
    """Updates an existing user."""
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        return None

    # Get fields to update (excluding None values)
    update_data = user_in.model_dump(exclude_unset=True)

    # Handle password update separately
    if "password" in update_data and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        db_user.hashed_password = hashed_password
        del update_data["password"]  # Remove from dict to avoid direct assignment

    # Handle role updates
    if "role_ids" in update_data:
        role_ids = update_data.pop("role_ids")  # Get and remove role_ids
        # Clear existing roles for this user
        existing_links = db.execute(
            select(UserRoleLink).where(UserRoleLink.user_id == db_user.id)
        ).scalars().all()
        for link in existing_links:
            db.delete(link)
        # Add new roles if provided
        if role_ids:
            for role_id in role_ids:
                role = crud.role.get_role(db, role_id=role_id)
                if not role:
                    # Consider how to handle invalid role IDs during update
                    # Option 1: Raise error (consistent with create)
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Role with ID {role_id} not found during update.",
                    )
                    # Option 2: Ignore invalid IDs
                    # continue
                link = UserRoleLink(user_id=db_user.id, role_id=role.id)
                db.add(link)
        # Commit role changes before refreshing
        db.commit()

    # Update remaining fields
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, *, user_id: int) -> User | None:
    """Deletes a user."""
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    # The user object is expired after deletion, but we can return it
    # if needed (e.g., to confirm which user was deleted).
    # If returning the object, ensure relationships are handled or detached.
    # For simplicity, let's return the object as it was before deletion.
    return db_user
