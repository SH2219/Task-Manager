# app/models/comment.py
from sqlalchemy import Column, BigInteger, Text, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(BigInteger, primary_key=True, index=True)
    task_id = Column(BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    body = Column(Text, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    edited_at = Column(TIMESTAMP(timezone=True), nullable=True)

    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")