from pydantic import BaseModel
from typing import Optional

# Schema for the data encoded within the JWT token
class TokenData(BaseModel):
    username: Optional[str] = None
    # Add other fields like scopes if needed

# Schema for the response when requesting a token
class Token(BaseModel):
    access_token: str
    token_type: str