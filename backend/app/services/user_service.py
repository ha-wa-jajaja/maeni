from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user(self, user_id: int):
        """Get a user by ID."""
        user = (
            self.db.query(User)
            .filter(User.id == user_id, User.is_deleted == False)
            .first()
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    def get_user_by_firebase_uid(self, firebase_uid: str):
        """Get a user by Firebase UID."""
        user = (
            self.db.query(User)
            .filter(User.firebase_uid == firebase_uid, User.is_deleted == False)
            .first()
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    def get_users(self, skip: int = 0, limit: int = 100):
        """Get all non-deleted users with pagination."""
        return (
            self.db.query(User)
            .filter(User.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_user(self, user: UserCreate):
        """Create a new user."""
        # Check if user with firebase_uid already exists
        db_user = (
            self.db.query(User).filter(User.firebase_uid == user.firebase_uid).first()
        )
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

        # Create new user
        db_user = User(
            firebase_uid=user.firebase_uid,
            display_name=user.display_name,
            email=user.email,
            role_id=user.role_id,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user_update: UserUpdate):
        """Update a user."""
        db_user = self.get_user(user_id)

        # Update fields if provided
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        """Soft delete a user."""
        db_user = self.get_user(user_id)
        db_user.is_deleted = True
        self.db.commit()
        return None
