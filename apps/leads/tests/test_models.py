import pytest

from apps.leads.models import Lead, VerticalPlaceholder


@pytest.mark.django_db
class TestVerticalPlaceholder:
    def test_str(self):
        vp = VerticalPlaceholder.objects.create(
            vertical="financial",
            headline="Coming Soon",
        )
        assert str(vp) == "Financial Services"

    def test_unique_vertical(self):
        VerticalPlaceholder.objects.create(vertical="farming")
        with pytest.raises(Exception):  # noqa: B017
            VerticalPlaceholder.objects.create(vertical="farming")


@pytest.mark.django_db
class TestLead:
    def test_str(self):
        lead = Lead.objects.create(
            vertical="energies",
            name="Test User",
            email="test@example.com",
        )
        assert str(lead) == "Test User (energies)"
