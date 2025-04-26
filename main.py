from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers and settings
from app.api.v1.endpoints import employees, auth, leave, department, position, user, role, branch # Import branch router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, # Use project name from settings
    description="Backend API for the HR System, now with a structured layout.",
    version="0.2.0"
)

# --- Middleware ---
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS], # Use settings
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# --- Routers ---
app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(leave.router) # Include leave router
app.include_router(department.router)
app.include_router(position.router)
app.include_router(user.router, prefix="/api/v1/users", tags=["users"]) # Add user router
app.include_router(role.router, prefix="/api/v1/roles", tags=["roles"]) # Add role router
app.include_router(branch.router, prefix="/api/v1/branches", tags=["branches"]) # Add branch router
# Add other routers here (e.g., departments, internal) as needed

@app.get("/")
async def read_root():
    """
    Root endpoint providing a welcome message.
    """
    return {"message": "Welcome to the Restructured HR System API"}

# --- Optional: Add global dependencies or middleware here if needed ---
# Example: app.add_middleware(...)
# Example: app.add_event_handler("startup", ...)