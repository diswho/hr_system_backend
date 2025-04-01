from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.models.leave import LeaveRequest
from app.schemas.leave import LeaveRequestCreate, LeaveStatus

def get_leave_request(db: Session, request_id: int) -> Optional[LeaveRequest]:
    """
    Retrieves a single leave request by its ID.
    """
    return db.query(LeaveRequest).filter(LeaveRequest.id == request_id).first()

def get_leave_requests(db: Session, skip: int = 0, limit: int = 100) -> List[LeaveRequest]:
    """
    Retrieves a list of leave requests with pagination.
    """
    return db.query(LeaveRequest).offset(skip).limit(limit).all()

def get_leave_requests_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100) -> List[LeaveRequest]:
    """
    Retrieves a list of leave requests for a specific employee with pagination.
    """
    return db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee_id).offset(skip).limit(limit).all()

def create_leave_request(db: Session, leave_request: LeaveRequestCreate) -> LeaveRequest:
    """
    Creates a new leave request in the database.
    Status defaults to PENDING.
    """
    db_leave_request = LeaveRequest(
        **leave_request.model_dump(),
        status=LeaveStatus.PENDING # Explicitly set default status
    )
    db.add(db_leave_request)
    db.commit()
    db.refresh(db_leave_request)
    return db_leave_request

# TODO: Add functions for updating status and deleting requests
# def update_leave_request_status(db: Session, request_id: int, status: LeaveStatus) -> Optional[LeaveRequest]: ...
# def delete_leave_request(db: Session, request_id: int) -> Optional[LeaveRequest]: ...