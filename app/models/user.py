# app/models/user.py
from sqlalchemy import Column, BigInteger, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(Text, unique=True, nullable=False, index=True)
    name = Column(Text, nullable=True)
    password_hash = Column(Text, nullable=True)
    timezone = Column(Text, server_default="UTC")
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
     # relationships (backrefs defined on other models)
    projects = relationship("Project", back_populates="owner", lazy="noload")
    created_tasks = relationship("Task", back_populates="creator", lazy="noload")