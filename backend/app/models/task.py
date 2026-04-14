import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.pending, nullable=False)
    priority: Mapped[TaskPriority] = mapped_column(Enum(TaskPriority), default=TaskPriority.medium, nullable=False)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=func.now())

    owner = relationship("User", back_populates="tasks")
