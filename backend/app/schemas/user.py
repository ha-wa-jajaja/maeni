from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base schema for user data validation."""

    display_name: Optional[str] = None
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a new user."""

    firebase_uid: str
    role_id: int = 1  # Default to regular user role


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    display_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role_id: Optional[int] = None


class UserResponse(UserBase):
    """Schema for user response."""

    id: int
    firebase_uid: str
    role_id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False

    class Config:
        orm_mode = True
