from pydantic import BaseModel, Field, ConfigDict
from typing import List

from .role import RoleRead # Import the Role schema for reading

# --- Pydantic Models for Authentication/Users ---


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: List[str] = []  # For role-based access later


# Removed old UserRole class, using RoleRead now


class UserBase(BaseModel):
    username: str = Field(..., min_length=3)
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    # Roles will be populated from the relationship via UserRoleLink
    roles: List[RoleRead] = []

    # Add Config class to enable ORM mode (from_attributes)
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel): # Inherit directly from BaseModel for creation
    # Fields required for creation
    username: str = Field(..., min_length=3)
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = False # Default to False
    password: str = Field(..., min_length=8)
    # Accept role IDs during creation
    role_ids: List[int] | None = None


class UserInDB(UserBase): # Inherits roles from UserBase
    hashed_password: str  # Stored in the database


class UserUpdate(BaseModel):
    """Schema for updating a user. All fields are optional."""
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    password: str | None = Field(default=None, min_length=8) # Optional password update
    role_ids: List[int] | None = None # Optional role update