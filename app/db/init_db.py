from sqlmodel import SQLModel # Import SQLModel
from app.db.session import engine
# Base is no longer needed as models inherit from SQLModel
from app.db.models import employee, leave, department, position, role, user, user_role_link  # Import all models so SQLModel discovers them


def init_db():
    """Initialize database by creating all tables"""
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine) # Use SQLModel's metadata
    print("Database tables created successfully")


if __name__ == "__main__":
    init_db()
