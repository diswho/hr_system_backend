from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

# Forward references for relationships
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .employee import Employee
    from .user import User

class Branch(SQLModel, table=True):
    __tablename__ = "branches"

    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True, unique=True, max_length=100) # Added unique and max_length
    address: str | None = Field(default=None, max_length=255) # Added max_length
    is_active: bool = Field(default=True)

    # Relationships: One Branch can have many Employees and Users
    employees: List["Employee"] = Relationship(back_populates="branch")
    users: List["User"] = Relationship(back_populates="branch")

    def __repr__(self):
        return f"<Branch(id={self.id}, name='{self.name}')>"