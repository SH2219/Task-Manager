# app/models/tag.py
from sqlalchemy import Column, BigInteger, Text, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(Text, nullable=False, index=True)
    owner_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Optionally, you can create back_populates relationships if needed
    owner = relationship("User", back_populates="tags")