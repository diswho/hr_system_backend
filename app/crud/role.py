from sqlalchemy.orm import Session # Use SQLAlchemy Session type hint
from sqlmodel import select # Keep select from sqlmodel
from typing import List

from app.db.models.role import Role
from app.schemas.role import RoleCreate

def get_role(db: Session, role_id: int) -> Role | None:
    """Gets a single role by ID."""
    role = db.get(Role, role_id)
    return role

def get_role_by_name(db: Session, name: str) -> Role | None:
    """Gets a single role by name."""
    statement = select(Role).where(Role.name == name)
    result = db.execute(statement)
    role = result.scalars().first()
    return role

def get_roles(db: Session, skip: int = 0, limit: int = 100) -> List[Role]:
    """Gets multiple roles with pagination."""
    statement = select(Role).offset(skip).limit(limit)
    result = db.execute(statement)
    roles = result.scalars().all()
    return roles

def create_role(db: Session, *, role_in: RoleCreate) -> Role:
    """Creates a new role."""
    db_role = Role.model_validate(role_in) # Use model_validate for SQLModel >= 0.0.14
    # For older SQLModel: db_role = Role.from_orm(role_in)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

# TODO: Implement update_role and delete_role functions if needed
# def update_role(...)
# def delete_role(...)