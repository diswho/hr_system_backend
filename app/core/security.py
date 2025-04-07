import os
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# Import models from the new location
from app.schemas.token import Token, TokenData
from app.schemas.user import UserInDB # UserRole removed
# Import settings
from app.core.config import settings

# --- Configuration (Now loaded from settings) ---
ALGORITHM = "HS256" # Keep algorithm hardcoded for now, or add to Settings

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- OAuth2 Scheme ---
# tokenUrl points to the endpoint that provides the token (defined in routers.auth)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token") # Updated tokenUrl path

# --- Utility Functions ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

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

# --- Mock User Database (Replace with real DB access) ---
# This is highly insecure and just for demonstration!
# TODO: Move this to a separate data layer or database module
# Initialize with the superuser from settings
fake_users_db: dict[str, UserInDB] = {
    settings.FIRST_SUPERUSER: UserInDB(
        id=1, # Added ID
        username=settings.FIRST_SUPERUSER,
        full_name="Admin User",
        email=settings.FIRST_SUPERUSER,
        hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
        disabled=False,
        # Mock roles matching RoleRead structure (at least id and name)
        roles=[{"id": 1, "name": "admin"}, {"id": 2, "name": "manager"}, {"id": 3, "name": "employee"}]
    ),
     "manager1": UserInDB(
        id=2, # Added ID
        username="manager1",
        full_name="Manager One",
        email="manager1@example.com",
        hashed_password=get_password_hash("managerpass"),
        disabled=False,
        roles=[{"id": 2, "name": "manager"}, {"id": 3, "name": "employee"}]
    ),
    "employee1": UserInDB(
        id=3, # Added ID
        username="employee1",
        full_name="Employee One",
        email="employee1@example.com",
        hashed_password=get_password_hash("employeepass"),
        disabled=False,
        roles=[{"id": 3, "name": "employee"}]
    )
}

def get_user(username: str) -> Optional[UserInDB]:
    """Retrieves a user from the fake database."""
    # TODO: Replace with actual database query
    if username in fake_users_db:
        user_data = fake_users_db[username]
        # Ensure we return a UserInDB instance, Pydantic might handle this if dict is compatible
        # but explicit instantiation is safer if needed.
        return UserInDB(**user_data.model_dump())
    return None

# --- Authentication Function ---
def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticates a user by checking username and password."""
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# --- Dependencies for Getting Current User ---
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    """Decodes the token, validates credentials, and returns the user."""
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

    user = get_user(username=token_data.username)
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
        if not any(role.name == required_role for role in current_user.roles):
            # Allow admins implicitly
            if not any(role.name == "admin" for role in current_user.roles):
                 raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User does not have the required '{required_role}' or 'admin' role"
                )
        return current_user
    return role_checker