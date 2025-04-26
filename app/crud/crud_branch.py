from sqlmodel import Session, select # Import Session and select from sqlmodel

from app.db.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchUpdate

def get_branch(db: Session, branch_id: int) -> Branch | None:
    # Use db.get() for primary key lookup if preferred and available
    # return db.get(Branch, branch_id)
    statement = select(Branch).where(Branch.id == branch_id)
    return db.exec(statement).first()

def get_branch_by_name(db: Session, name: str) -> Branch | None:
    statement = select(Branch).where(Branch.name == name)
    return db.exec(statement).first()

def get_branches(db: Session, skip: int = 0, limit: int = 100) -> list[Branch]:
    statement = select(Branch).offset(skip).limit(limit)
    return db.exec(statement).all()

def create_branch(db: Session, branch: BranchCreate) -> Branch:
    # SQLModel automatically handles attribute assignment from Pydantic models
    db_branch = Branch.model_validate(branch) # Use model_validate for Pydantic v2+
    # Or: db_branch = Branch(**branch.dict()) for older Pydantic
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

def update_branch(db: Session, db_branch: Branch, branch_in: BranchUpdate) -> Branch:
    branch_data = branch_in.model_dump(exclude_unset=True) # Use model_dump for Pydantic v2+
    for key, value in branch_data.items():
        setattr(db_branch, key, value)
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

def delete_branch(db: Session, branch_id: int) -> Branch | None:
    db_branch = db.get(Branch, branch_id) # Use db.get() for efficiency
    # Or use the previous select method if db.get isn't suitable
    # statement = select(Branch).where(Branch.id == branch_id)
    # db_branch = db.exec(statement).first()
    if db_branch:
        db.delete(db_branch)
        db.commit()
        # Optionally return the deleted object or a confirmation
        return db_branch
    return None # Indicate branch not found