from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from sqlalchemy.orm import Session # Import Session

# Import schemas, security functions, and settings
from app.schemas.token import Token
from app.schemas.user import UserInDB
from app.core.security import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from app.core.config import settings # Import settings

router = APIRouter(
    prefix="/auth", # Changed prefix to /auth
    tags=["authentication"],
)
from app.db.session import get_db # Import get_db dependency

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db) # Add DB session dependency
):
    """
    Provides an access token for valid user credentials.

    Uses OAuth2 Password Flow.
    """
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password) # Pass db session
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) # Use settings
    access_token = create_access_token(
        data={"sub": user.username, "scopes": [role.name for role in user.roles]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=UserInDB)
async def read_users_me(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    """
    Gets the current logged-in user's details.

    Requires authentication.
    """
    return current_user