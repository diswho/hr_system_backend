from pydantic import BaseModel, ConfigDict
from typing import Optional

# Shared properties
class BranchBase(BaseModel):
    name: str
    address: Optional[str] = None
    is_active: Optional[bool] = True

# Properties to receive via API on creation
class BranchCreate(BranchBase):
    pass

# Properties to receive via API on update
class BranchUpdate(BranchBase):
    name: Optional[str] = None # Allow partial updates

# Properties shared by models stored in DB
class BranchInDBBase(BranchBase):
    id: int
    model_config = ConfigDict(from_attributes=True) # Use orm_mode in older Pydantic versions

# Properties to return to client
class Branch(BranchInDBBase):
    pass

# Properties stored in DB
class BranchInDB(BranchInDBBase):
    pass