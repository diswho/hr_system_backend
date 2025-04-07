from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional

# Forward references for relationships
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .employee import Employee
    from .role import Role
    from .user_role_link import UserRoleLink


# Note: Storing roles directly in the User table (e.g., as JSON) is simple but less flexible
# than having a separate Role table and a User-Role link table.
# For now, we assume roles aren't directly stored as structured data in this table.
# The `roles` field from the Pydantic schema is handled at the API/schema level.

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True, index=True)
    username: str = Field(index=True, unique=True, min_length=3)
    email: str | None = Field(default=None, index=True)  # Make email unique if required
    full_name: str | None = Field(default=None)
    hashed_password: str = Field()
    disabled: bool | None = Field(default=False)

    # Relationship to Employee (optional one-to-one)
    # Assumes Employee model has: user: Optional["User"] = Relationship(back_populates="employee_profile")
    employee_profile: Optional["Employee"] = Relationship(back_populates="user") # sa_relationship_kwargs={"uselist": False} might be needed if Employee.user isn't Optional

    # Relationship to the link table (UserRoleLink)
    role_links: List["UserRoleLink"] = Relationship(back_populates="user")
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

# TODO: Consider if roles need to be a separate table/model and relationship
# Example if Employee needs a user_id foreign key:
# In app/db/models/employee.py:
# class Employee(...):
#    ...
#    user_id: int | None = Field(default=None, foreign_key="users.id")
#    user: "User" | None = Relationship(back_populates="employee_profile")
