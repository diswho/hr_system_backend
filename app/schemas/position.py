from pydantic import BaseModel, Field
from typing import Optional

class PositionBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: Optional[str] = Field(None, max_length=255)

class PositionCreate(PositionBase):
    pass

class Position(PositionBase):
    id: int

    class Config:
        from_attributes = True

# class PositionUpdate(BaseModel)
class PositionUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=255)