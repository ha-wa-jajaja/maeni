import pytest
from app.auth import get_current_user

# This file contains shared fixtures for tests


@pytest.fixture(autouse=True)
def override_dependencies():
    """
    Override dependencies for testing.
    This fixture runs automatically for all tests.
    """
    # This is set up in each test module based on needs
    pass
