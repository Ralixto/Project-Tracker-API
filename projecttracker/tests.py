import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Project, User

@pytest.mark.django_db
def test_unauthenticated_get_project():
    client = APIClient()
    response = client.get('/project/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_unauthenticated_post_project():
    client = APIClient()

    payload = {
            "name": "Task3",
            "owner": "1",
            "members": [1],
            "description": "Task2",
            "status": "COMP",
            "priority": "",
            "budget": "123",
            "risk_level": "L",
            "start_date": "2026-08-09",
            "end_date": "2027-08-09"
    }

    response = client.post('/project/', data=payload)
    assert response.status_code == 401

@pytest.mark.django_db
def test_authenticated_post_project():
    client = APIClient()
    user = User.objects.create_user(username="Test", password="Testuser1")

    payload = {
            "name": "Task3",
            "owner": "1",
            "members": [1],
            "description": "Task2",
            "status": "COMP",
            "priority": "",
            "budget": "123",
            "risk_level": "L",
            "start_date": "2026-08-09",
            "end_date": "2027-08-09"
    }

    client.force_authenticate(user=user)

    response = client.post('/project/', data=payload)
    assert response.status_code == 201

@pytest.mark.django_db
def test_user_edit_another_user_post():
    owner = User.objects.create_user(username="Test", password="Testuser1")
    attacker = User.objects.create_user(username="Test2", password="Testuser2")

    project = Project.objects.create(
        name="Task3",
        owner=owner,
        description="Task2",
        status="COMP",
        priority="M",
        budget="123",
        risk_level="L",
        start_date="2026-08-09",
        end_date="2027-08-09"   
    )

    project.members.set([owner])

    payload = {
        "name": "Task323",
        "description": "Tasks2",
        "members": [owner.id],
        "status": "COMP",
        "priority": "L",
        "budget": "123",
        "risk_level": "L",
        "start_date": "2026-08-09",
        "end_date": "2027-08-09"
    }

    client = APIClient()
    client.force_authenticate(user=attacker)

    response = client.put(f"/project/{project.id}/", data=payload, format="json")
    assert response.status_code == 403

@pytest.mark.django_db
def test_project_health_get():
    client = APIClient()
    response = client.get('/project/health/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_api_register_post():
    payload = {
        "username": "Testuser22",
        "email": "testuser22@gmail.com",
        "password": "Testuser22",
        "password2": "Testuser22"
    }

    client = APIClient()
    response = client.post('/api/register/', data=payload)
    assert response.status_code == 201

@pytest.mark.django_db
def test_api_register_mismatched_passwords_post():
    payload = {
        "username": "Testuser22",
        "email": "testuser22@gmail.com",
        "password": "Testuser22",
        "password2": "Testuser22wdf"
    }

    client = APIClient()
    response = client.post('/api/register/', data=payload)
    assert response.status_code == 400