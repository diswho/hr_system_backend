from pydantic import BaseModel
from typing import List

# --- Pydantic Models for Roles ---

# Properties shared by models stored in DB
class RoleBase(BaseModel):
    name: str
    description: str | None = None

# Properties to receive via API on creation
class RoleCreate(RoleBase):
    pass # No extra fields needed for creation currently

# Properties to return to client
class RoleRead(RoleBase):
    id: int

    # If you want to show users associated with a role (can be heavy)
    # users: List["UserRead"] = [] # Requires UserRead schema and careful handling

    class Config:
        from_attributes = True # For compatibility with ORM models

# Properties stored in DB
class RoleInDB(RoleBase):
    id: int

# --- Schemas for User-Role linking (if needed directly in API) ---
# Usually, roles are managed as part of the User object in the API

# Example: Schema to represent a role linked to a user
# class UserRole(BaseModel):
#     role_id: int
#     name: str # Include role name for convenience