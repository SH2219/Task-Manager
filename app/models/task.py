# app/models/task.py
from sqlalchemy import (
    Column, BigInteger, Integer, SmallInteger, Text, Boolean,
    TIMESTAMP, func, ForeignKey, Table, Index
)

from sqlalchemy.orm import relationship

from app.db.base import Base

# Association table: task_assignments (many-to-many Task <-> User)
task_assignments = Table(
    "task_assignments",
    Base.metadata,
    Column("task_id", BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("assigned_by", BigInteger, ForeignKey("users.id"), nullable=True),
    Column("assigned_at", TIMESTAMP(timezone=True), server_default=func.now()),
)

# Association table: task_tags (many-to-many Task <-> Tag)

task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", BigInteger, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ =(
        Index("ix_tasks_project_id_status", "project_id", "status", "due_at"),
    )
    
    id = Column(BigInteger, primary_key=True, index=True)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    creator_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Text, nullable=False, server_default="todo")
    priority = Column(SmallInteger, server_default="3")
    due_at = Column(TIMESTAMP(timezone=True), nullable=True)
    start_at = Column(TIMESTAMP(timezone=True), nullable=True)
    estimated_minutes = Column(Integer, nullable=True)
    
    parent_task_id = Column(BigInteger, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    position = Column(Integer, server_default="0")
    version = Column(Integer, server_default="1")  # optimistic locking
    is_deleted = Column(Boolean, server_default="false")
    
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
     # relationships
    project = relationship("Project", back_populates="tasks")
    creator = relationship("User", back_populates="created_tasks", foreign_keys=[creator_id])


      # many-to-many / associations
    assignees = relationship("User", secondary=task_assignments, lazy="select")
    tags = relationship("Tag", secondary=task_tags, lazy="select")

    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="task", cascade="all, delete-orphan")

    # self-referential parent/children
    parent = relationship("Task", remote_side=[id], backref="subtasks")