from sqlmodel import Field, Relationship, SQLModel

# Forward references for relationships
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import User
    from .role import Role

class UserRoleLink(SQLModel, table=True):
    __tablename__ = "user_role_link" # Optional: customize table name if needed

    user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    role_id: int | None = Field(default=None, foreign_key="roles.id", primary_key=True)

    # Relationships back to User and Role
    user: "User" = Relationship(back_populates="role_links")
    role: "Role" = Relationship(back_populates="user_links")