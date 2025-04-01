from fastapi import APIRouter

from app.api.v1.endpoints import employees, auth, leave, department, position

router = APIRouter()
router.include_router(employees.router, prefix="/employees", tags=["employees"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(leave.router, prefix="/leave", tags=["leave"])
router.include_router(department.router, prefix="/departments", tags=["departments"])
router.include_router(position.router, prefix="/positions", tags=["positions"])