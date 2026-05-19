"""Admin smoke tests — verify each construction admin changelist loads for a staff user."""

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from apps.construction.models import (
    Certification,
    ConstructionService,
    Project,
    Testimonial,
)


@pytest.fixture
def admin_client(db):
    User = get_user_model()
    user = User.objects.create_user(
        username="admin", password="testpass", is_staff=True, is_superuser=True
    )
    client = Client()
    client.force_login(user)
    return client


@pytest.mark.django_db
class TestConstructionAdmins:
    def test_service_changelist_loads(self, admin_client):
        ConstructionService.objects.create(name="Test Service", summary="x")
        response = admin_client.get(reverse("admin:construction_constructionservice_changelist"))
        assert response.status_code == 200
        assert b"Test Service" in response.content

    def test_project_changelist_loads(self, admin_client):
        Project.objects.create(
            title="Test Project",
            sector="residential",
            location_city="Dar",
            year_completed=2024,
        )
        response = admin_client.get(reverse("admin:construction_project_changelist"))
        assert response.status_code == 200
        assert b"Test Project" in response.content
        # Sector pill rendered
        assert b"Residential" in response.content

    def test_testimonial_changelist_loads(self, admin_client):
        Testimonial.objects.create(author_name="Test Author", quote="Quote here.")
        response = admin_client.get(reverse("admin:construction_testimonial_changelist"))
        assert response.status_code == 200
        assert b"Test Author" in response.content

    def test_certification_changelist_loads(self, admin_client):
        Certification.objects.create(name="ISO 9001", issuer="ISO", year_awarded=2024)
        response = admin_client.get(reverse("admin:construction_certification_changelist"))
        assert response.status_code == 200
        assert b"ISO 9001" in response.content
