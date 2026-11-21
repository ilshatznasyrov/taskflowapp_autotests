import uuid
import pytest


@pytest.fixture(scope="session")
def user_data():
    unique_id = uuid.uuid4().hex[:8]

    return {
        "name": f"user_{unique_id}",
        "email": f"user_{unique_id}@example.ru",
        "password": "Test123",
    }
