from sqlmodel import Field, Relationship, SQLModel
from typing import List

# Forward references for relationships
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user_role_link import UserRoleLink # Link table model

class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True, unique=True, max_length=50)
    description: str | None = Field(default=None, max_length=255)

    # Relationship to the link table (UserRoleLink)
    user_links: List["UserRoleLink"] = Relationship(back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"