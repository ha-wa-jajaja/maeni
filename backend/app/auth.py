from app.database import get_db
from app.models.user import User
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

# Create a security scheme for JWT authentication
security = HTTPBearer()


# This is a placeholder for Firebase authentication
# You'll need to implement the actual Firebase auth verification later
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Placeholder for Firebase authentication.
    This will be replaced with actual Firebase token verification.
    """
    try:
        # Placeholder: In the actual implementation, you'd verify the Firebase token here
        # and extract the firebase_uid from the token

        # For now, this just finds the first user (for development purposes only)
        # In production, you'd get the firebase_uid from the verified token
        user = db.query(User).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
