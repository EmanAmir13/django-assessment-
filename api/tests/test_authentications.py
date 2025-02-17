import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """Fixture to create an API client."""
    return APIClient()


@pytest.fixture
def create_user(db):
    """Fixture to create a test user."""

    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return make_user


def test_register_user(api_client, db):
    """Test user registration API."""
    data = {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "username": "Test User"
    }
    response = api_client.post("/api/register/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email=data["email"]).exists()


def test_login_user(api_client, create_user):
    """Test user login API."""
    user = create_user(email="testuser@example.com", password="testpassword123", username="Test User")
    data = {"email": "testuser@example.com", "password": "testpassword123"}
    response = api_client.post("/api/login/", data)

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_invalid_credentials(api_client):
    """Test login with incorrect credentials."""
    data = {"email": "wrong@example.com", "password": "wrongpassword"}
    response = api_client.post("/api/login/", data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data == {"error": "Invalid Credentials"}
