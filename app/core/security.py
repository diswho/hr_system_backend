import os
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
# from passlib.context import CryptContext # Moved to hashing.py
from sqlalchemy.orm import Session # Import Session
from app.core.hashing import verify_password # Import from new hashing module

# Import models from the new location
from app.schemas.token import Token, TokenData
from app.schemas.user import UserInDB # Keep UserInDB
# from app.db.models.user import User # Don't need User model directly here anymore
from app import crud # Import crud module
from app.db.session import get_db # Import get_db dependency
# Import settings
from app.core.config import settings

# --- Configuration (Now loaded from settings) ---
ALGORITHM = "HS256" # Keep algorithm hardcoded for now, or add to Settings

# --- Password Hashing (Moved to app/core/hashing.py) ---
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Moved

# --- OAuth2 Scheme ---
# tokenUrl points to the endpoint that provides the token (defined in routers.auth)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token") # Updated tokenUrl path

# --- Utility Functions (Moved to app/core/hashing.py) ---
# def verify_password(plain_password: str, hashed_password: str) -> bool: # Moved
#     """Verifies a plain password against a hashed password.""" # Moved
#     return pwd_context.verify(plain_password, hashed_password) # Moved
#
# def get_password_hash(password: str) -> str: # Moved
#     """Hashes a plain password.""" # Moved
#     return pwd_context.hash(password) # Moved

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) # Use settings
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM) # Use settings
    return encoded_jwt

# --- Database User Retrieval ---
# Removed fake_users_db
def get_user(db: Session = Depends(get_db), username: str = "") -> UserInDB | None:
    """Retrieves a user from the database by username."""
    if not username: # Handle empty username case if necessary
        return None
    db_user = crud.user.get_user_by_username(db=db, username=username)
    if db_user:
        # Pydantic's from_attributes should handle the conversion
        # because crud.user.get_user_by_username now eagerly loads roles
        # and UserInDB expects roles: List[RoleRead]
        # However, Pydantic needs the actual Role objects, not UserRoleLink objects.
        # We need to extract the Role objects from the links.
        user_roles = [link.role for link in db_user.role_links if link.role] # Extract Role objects
        user_data = db_user.model_dump() # Get user data as dict
        user_data['roles'] = user_roles # Assign the extracted Role objects to the 'roles' key
        return UserInDB(**user_data) # Create UserInDB instance
    return None

# --- Authentication Function ---
# --- Authentication Function ---
# Note: The db session needs to be passed to this function from the caller (e.g., the token endpoint)
def authenticate_user(db: Session, username: str, password: str) -> UserInDB | None:
    """Authenticates a user by checking username and password against the DB."""
    user = get_user(db=db, username=username) # Pass db session to get_user
    if not user:
        return None
    if not verify_password(password, user.hashed_password): # Uses imported verify_password
        return None
    return user

# --- Dependencies for Getting Current User ---
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db) # Inject DB session here
) -> UserInDB:
    """Decodes the token, validates credentials, and returns the user from DB."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM]) # Use settings
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username) # Scopes could be extracted here too if needed
    except JWTError:
        raise credentials_exception

    # Use the modified get_user function which now requires a db session
    user = get_user(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
) -> UserInDB:
    """Checks if the current user is active."""
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

# --- Dependency for Role Checking ---
def require_role(required_role: str):
    """Dependency factory to check if the current user has a specific role."""
    async def role_checker(current_user: Annotated[UserInDB, Depends(get_current_active_user)]) -> UserInDB:
        # Access roles directly from the UserInDB object
        user_roles = current_user.roles
        if not any(role.name == required_role for role in user_roles):
            # Allow admins implicitly
            # if not any(role.name == "admin" for role in user_roles):
            #      raise HTTPException(
            #         status_code=status.HTTP_403_FORBIDDEN,
            #         detail=f"User does not have the required '{required_role}' or 'admin' role"
            #     )
            raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User does not have the required '{required_role}' role")
        return current_user
    return role_checker