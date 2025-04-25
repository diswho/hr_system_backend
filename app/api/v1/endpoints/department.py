from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.security import require_role
from app.db.session import get_db
from app.crud import crud_department
from app.schemas.department import Department, DepartmentCreate, DepartmentUpdate

router = APIRouter(prefix="/department",
                   tags=["department"],
                   dependencies=[Depends(require_role(["system"]))],  # Apply auth to all routes in this router
                   responses={404: {"description": "Not found"}},)


@router.post("/", response_model=Department)
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    return crud_department.create_department(db, department)


@router.get("/", response_model=List[Department])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_department.get_departments(db, skip=skip, limit=limit)


@router.get("/{department_id}", response_model=Department)
def read_department(department_id: int, db: Session = Depends(get_db)):
    department = crud_department.get_department(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.put("/{department_id}", response_model=Department)
def update_department(department_id: int, department: DepartmentUpdate, db: Session = Depends(get_db)):
    return crud_department.update_department(db, department_id, department)


@router.delete("/{department_id}", response_model=Department)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    return crud_department.delete_department(db, department_id)
