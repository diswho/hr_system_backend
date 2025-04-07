from typing import List

from sqlmodel import Field, Relationship, SQLModel

# Forward references for relationships
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .employee import Employee


class Position(SQLModel, table=True):
    __tablename__ = "positions"

    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=50, unique=True)
    description: str | None = Field(default=None, max_length=255)

    # Relationship to Employee (one-to-many)
    employees: List["Employee"] = Relationship(back_populates="position")

    def __repr__(self):
        return f"<Position(id={self.id}, name='{self.name}')>"