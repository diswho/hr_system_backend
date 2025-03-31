from pydantic import BaseModel, Field
from typing import Optional, List

# --- Pydantic Models for Authentication/Users ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = [] # For role-based access later

class UserRole(BaseModel): # Simple role model for now
    name: str

class UserBase(BaseModel):
    username: str = Field(..., min_length=3)
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    roles: List[UserRole] = [] # List of roles

class UserCreate(UserBase):
    password: str = Field(..., min_length=8) # Used for creating users (not implemented yet)

class UserInDB(UserBase):
    hashed_password: str # Stored in the database (or fake DB for now)