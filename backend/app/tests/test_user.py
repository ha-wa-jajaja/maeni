import pytest
from app.main import app  # Adjust import based on your project structure
from fastapi.testclient import TestClient

# Create a test client
client = TestClient(app)


def test_get_all_users_200_ok(get_token):
    """
    Test retrieving all users with a valid authentication token

    Assumptions:
    - get_token is a fixture that provides a valid authentication token
    - The endpoint is "/api/user/"
    - Successful response returns a list of users
    """
    response = client.get(
        "/api/user/", headers={"Authorization": f"Bearer {get_token}"}
    )

    # Assertions to validate the response
    assert response.status_code == 200

    # Optional: Check that the response contains users
    response_data = response.json()
    assert len(response_data) > 0, "Expected to receive at least one user"


def test_get_users_unauthorized():
    """
    Test that unauthenticated requests are rejected
    """
    response = client.get("/api/user/")
    assert response.status_code == 401, "Expected unauthorized access to be blocked"


# Add more tests as needed, such as:
# - Creating a user
# - Updating a user
# - Deleting a user
# - Retrieving a specific user
