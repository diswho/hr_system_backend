from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Schema for User Role
class UserRole(BaseModel):
    name: str

# Base schema with common attributes
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    roles: List[UserRole] = [] # Updated to use UserRole schema

# Schema for creating a user (used for input)
class UserCreate(UserBase):
    password: str

# Schema for reading/representing a user in API responses
class User(UserBase):
    id: int

    class Config:
        from_attributes = True # For ORM mode

# Schema representing a user as stored in the database
# Often includes fields like hashed_password
class UserInDB(User):
    hashed_password: str
    # Ensure roles here also uses UserRole if needed for consistency,
    # although it inherits from User which already has the updated roles.