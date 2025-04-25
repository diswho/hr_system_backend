from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.security import require_role # Added import

from app.db.session import get_db
from app.crud import crud_position
from app.schemas.position import Position, PositionCreate, PositionUpdate

router = APIRouter(
    prefix="/position",
    tags=["position"],
    dependencies=[Depends(require_role(["system", "admin"]))], # Apply role check to all routes
    responses={404: {"description": "Not found"}},
    )

@router.post("/", response_model=Position)
def create_position(position: PositionCreate, db: Session = Depends(get_db)):
    return crud_position.create_position(db, position)

@router.get("/", response_model=List[Position])
def read_positions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_position.get_positions(db, skip=skip, limit=limit)

@router.get("/{position_id}", response_model=Position)
def read_position(position_id: int, db: Session = Depends(get_db)):
    position = crud_position.get_position(db, position_id)
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position

@router.put("/{position_id}", response_model=Position)
def update_position(position_id: int, position: PositionUpdate, db: Session = Depends(get_db)):
    return crud_position.update_position(db, position_id, position)

@router.delete("/{position_id}", response_model=Position)
def delete_position(position_id: int, db: Session = Depends(get_db)):
    return crud_position.delete_position(db, position_id)