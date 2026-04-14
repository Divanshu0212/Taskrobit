from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

from app.models.user import UserRole


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    username: str | None = None

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if len(value) < 3 or len(value) > 50:
            raise ValueError("Username must be 3-50 characters")
        return value


class UserRoleUpdate(BaseModel):
    role: UserRole


class UserStatusUpdate(BaseModel):
    is_active: bool
