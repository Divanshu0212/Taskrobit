from datetime import datetime

from pydantic import BaseModel, field_validator

from app.models.task import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: TaskPriority = TaskPriority.medium
    due_date: datetime | None = None

    @field_validator("title")
    @classmethod
    def title_length(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2 or len(value) > 200:
            raise ValueError("Title must be 2-200 characters")
        return value


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None
    owner_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
