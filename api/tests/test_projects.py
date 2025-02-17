import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from api.models import Project

User = get_user_model()


@pytest.fixture
def api_client():
    """Fixture to create an API client."""
    return APIClient()


@pytest.fixture
def admin_user(db):
    """Fixture to create an admin user."""
    return User.objects.create_user(email="admin@example.com", username="Admin", password="adminpass", role="admin")


@pytest.fixture
def regular_user(db):
    """Fixture to create a regular user."""
    return User.objects.create_user(email="user@example.com", username="User", password="userpass", role="member")


@pytest.fixture
def mock_access_token(admin_user):
    """Fixture to generate a mock access token for authentication."""
    token = AccessToken.for_user(admin_user)
    return str(token)


@pytest.fixture
def regular_user_token(regular_user):
    """Fixture to generate a mock access token for a regular user."""
    token = AccessToken.for_user(regular_user)
    return str(token)


@pytest.fixture
def authenticated_client(api_client, mock_access_token):
    """Fixture to authenticate the API client with a mock access token."""
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {mock_access_token}")
    return api_client


@pytest.fixture
def regular_authenticated_client(api_client, regular_user_token):
    """Fixture to authenticate the API client with a regular user's access token."""
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {regular_user_token}")
    return api_client


@pytest.fixture
def create_project(db, admin_user):
    """Fixture to create a project."""
    return Project.objects.create(title="Test Project", description="Test Description", creator=admin_user)


@pytest.mark.django_db
def test_create_project_as_admin(authenticated_client):
    """Test creating a project as an admin user with a mocked access token."""
    data = {"title": "New Project", "description": "New Description"}
    response = authenticated_client.post("/api/projects/", data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Project.objects.filter(title="New Project").exists()


@pytest.mark.django_db
def test_regular_user_cannot_create_project(regular_authenticated_client):
    """Test that a regular user cannot create a project."""
    data = {"title": "Unauthorized Project", "description": "Should not be created"}
    response = regular_authenticated_client.post("/api/projects/", data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not Project.objects.filter(title="Unauthorized Project").exists()


@pytest.mark.django_db
def test_admin_can_delete_project(authenticated_client, create_project):
    """Test that an admin can delete a project."""
    project_id = create_project.id
    response = authenticated_client.delete(f"/api/projects/{project_id}/")

    assert response.status_code == status.HTTP_200_OK
    assert not Project.objects.filter(id=project_id).exists()
    assert response.data["message"] == f"Project '{create_project.title}' has been deleted successfully."
