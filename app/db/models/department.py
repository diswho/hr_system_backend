from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.name}')>"