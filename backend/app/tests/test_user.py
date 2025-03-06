from unittest.mock import MagicMock, patch

import pytest
from app.auth import get_current_user
from app.database import Base, get_db
from app.main import app
from app.models.user import Role, User
from app.services.user_service import UserService
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Set up test client with overridden dependencies
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create test data
    db = TestingSessionLocal()

    # Create a role
    test_role = Role(id=1, name="User")
    db.add(test_role)

    # Create a test user
    global test_user
    test_user = User(
        id=1,
        firebase_uid="test_firebase_uid",
        display_name="Test User",
        email="test@example.com",
        role_id=1,
    )
    db.add(test_user)

    db.commit()

    # Set up dependency override for get_current_user
    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    yield db

    # Clean up
    Base.metadata.drop_all(bind=engine)


def test_create_user(test_db):
    # Test creating a new user
    response = client.post(
        "/users/",
        json={
            "firebase_uid": "new_firebase_uid",
            "display_name": "New User",
            "email": "new@example.com",
            "role_id": 1,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["firebase_uid"] == "new_firebase_uid"
    assert data["display_name"] == "New User"
    assert data["email"] == "new@example.com"

    # Check if user was actually created in database
    user_service = UserService(test_db)
    db_user = user_service.get_user_by_firebase_uid("new_firebase_uid")
    assert db_user is not None
    assert db_user.display_name == "New User"


def test_read_users(test_db):
    # Test reading all users
    response = client.get("/users/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1  # At least the test user should be there
    assert any(user["firebase_uid"] == "test_firebase_uid" for user in data)


def test_read_user(test_db):
    # Test reading a specific user
    response = client.get("/users/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["firebase_uid"] == "test_firebase_uid"
    assert data["display_name"] == "Test User"


def test_update_user(test_db):
    # Test updating a user
    response = client.put("/users/1", json={"display_name": "Updated User"})

    assert response.status_code == 200
    data = response.json()
    assert data["display_name"] == "Updated User"

    # Check if user was actually updated in database
    user_service = UserService(test_db)
    db_user = user_service.get_user(1)
    assert db_user.display_name == "Updated User"


def test_delete_user(test_db):
    # Test deleting a user (soft delete)
    response = client.delete("/users/1")

    assert response.status_code == 204

    # Check if user was actually soft deleted in database
    # Need to query directly since get_user filters out deleted users
    db_user = test_db.query(User).filter(User.id == 1).first()
    assert db_user.is_deleted == True


@pytest.mark.parametrize(
    "user_id,expected_status_code",
    [
        (999, 404),  # Non-existent user
    ],
)
def test_read_user_not_found(test_db, user_id, expected_status_code):
    # Test reading a non-existent user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "firebase_uid,expected_status_code",
    [
        ("non_existent_uid", 404),  # Non-existent user
    ],
)
def test_read_user_by_firebase_not_found(test_db, firebase_uid, expected_status_code):
    # Test reading a non-existent user by Firebase UID
    response = client.get(f"/users/by-firebase/{firebase_uid}")
    assert response.status_code == expected_status_code
