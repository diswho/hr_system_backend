from app.db.session import engine
from app.db.session import Base
from app.db.models import employee, leave,department,position  # Import all models

def init_db():
    """Initialize database by creating all tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

if __name__ == "__main__":
    init_db()