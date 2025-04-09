from sqlmodel import SQLModel, Session, select  # Third-party imports
from app.db.session import engine  # Local imports
# Import all models so SQLModel discovers them
from app.db.models import (
    employee, leave, department,
    position, role, user, user_role_link
)
from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.user_role_link import UserRoleLink
from app.core.hashing import get_password_hash


def init_db():
    """Initialize database by creating all tables and adding initial data"""
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine) # Use SQLModel's metadata
    print("Database tables created successfully")
    
    with Session(engine) as session:
        # Create system role if it doesn't exist
        if not session.get(Role, 1):
            system_role = Role(
                id=1,
                name="system",
                description="system"
            )
            session.add(system_role)
            session.commit()
            print("System role created successfully")
        
        # Create admin user if it doesn't exist
        if not session.get(User, 1):
            admin = User(
                username="system",
                email="system@email.com",
                full_name="System",
                hashed_password=get_password_hash("ChangeMe123"),
                disabled=False
            )
            session.add(admin)
            session.commit()
            print("System user created successfully (temporary password: ChangeMe123)")

        # Link admin user to system role if not already linked
        if not session.exec(select(UserRoleLink).where(
            UserRoleLink.user_id == 1,
            UserRoleLink.role_id == 1
        )).first():
            user_role_link = UserRoleLink(
                user_id=1,
                role_id=1
            )
            session.add(user_role_link)
            session.commit()
            print("System user linked to system role successfully")


if __name__ == "__main__":
    init_db()
