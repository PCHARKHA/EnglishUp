from sqlalchemy import Column,Integer,String
from app.db.base import Base
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False,index=True)
    hashed_password = Column(String, nullable=False)
    job_role = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    transcripts = relationship(
        "Transcript",
        back_populates="user",
        cascade="all, delete-orphan"
    )

