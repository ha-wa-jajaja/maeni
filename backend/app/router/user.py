from typing import List

from app.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas import user as user_schema
from app.services.user_service import UserService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=user_schema.UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    user_service = UserService(db)
    return user_service.create_user(user=user)


@router.get("/", response_model=List[user_schema.UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all users."""
    user_service = UserService(db)
    return user_service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=user_schema.UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific user by ID."""
    user_service = UserService(db)
    return user_service.get_user(user_id=user_id)


@router.get("/by-firebase/{firebase_uid}", response_model=user_schema.UserResponse)
def read_user_by_firebase(firebase_uid: str, db: Session = Depends(get_db)):
    """Get a user by their Firebase UID."""
    user_service = UserService(db)
    return user_service.get_user_by_firebase_uid(firebase_uid=firebase_uid)


@router.put("/{user_id}", response_model=user_schema.UserResponse)
def update_user(
    user_id: int,
    user_update: user_schema.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a user."""
    user_service = UserService(db)
    return user_service.update_user(user_id=user_id, user_update=user_update)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Soft delete a user."""
    user_service = UserService(db)
    user_service.delete_user(user_id=user_id)
    return None
