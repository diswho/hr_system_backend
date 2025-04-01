from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings # Import settings to get DB URL

# Create the SQLAlchemy engine using the database URL from settings
# The pool_pre_ping=True argument helps handle dropped connections
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Optional: Function to create all tables (useful for initial setup/testing)
# Be cautious using this in production with migrations (e.g., Alembic)
# def init_db():
#     # Import all models here before calling create_all
#     # from app.db.models import user, employee, leave # Example
#     Base.metadata.create_all(bind=engine)