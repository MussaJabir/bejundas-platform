import pytest

from apps.leads.models import Lead, VerticalPlaceholder


@pytest.mark.django_db
class TestVerticalPlaceholder:
    def test_str(self):
        # Seeded by migration — fetch rather than create
        vp = VerticalPlaceholder.objects.get(vertical="financial")
        assert str(vp) == "Financial Services"

    def test_unique_vertical(self):
        # "farming" already exists from the seed migration; trying to create a second must fail
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
