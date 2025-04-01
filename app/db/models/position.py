from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Position(Base):
    __tablename__ = "positions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<Position(id={self.id}, name='{self.name}')>"