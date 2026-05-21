import pytest
from django.test import Client

from apps.leads.models import Lead, VerticalPlaceholder

# Phase-1 of the financial vertical moved /financial/ off the Coming Soon
# view (now served by apps.financial). Phase-1 of farming did the same for
# /farming/ (now served by apps.farming). These tests exercise the
# remaining placeholder verticals /energies/ and /investments/ to verify
# the lead-capture Coming Soon page still works.


@pytest.fixture
def energies_placeholder(db):
    return VerticalPlaceholder.objects.get(vertical="energies")


@pytest.mark.django_db
class TestComingSoonView:
    def test_known_vertical_returns_200(self, energies_placeholder):
        response = Client().get("/energies/")
        assert response.status_code == 200

    def test_uses_coming_soon_template(self, energies_placeholder):
        response = Client().get("/energies/")
        assert "leads/coming_soon.html" in [t.name for t in response.templates]

    def test_placeholder_in_context(self, energies_placeholder):
        response = Client().get("/energies/")
        assert response.context["placeholder"] == energies_placeholder

    def test_inactive_placeholder_not_shown(self, db):
        VerticalPlaceholder.objects.filter(vertical="investments").update(is_active=False)
        try:
            response = Client().get("/investments/")
            assert response.context["placeholder"] is None
        finally:
            VerticalPlaceholder.objects.filter(vertical="investments").update(is_active=True)

    def test_valid_form_creates_lead(self, energies_placeholder):
        Client().post(
            "/energies/",
            {
                "name": "Amina Hassan",
                "email": "amina@example.com",
                "phone": "+255712345678",
                "message": "Interested in your services.",
            },
        )
        lead = Lead.objects.get(email="amina@example.com")
        assert lead.vertical == "energies"
        assert lead.name == "Amina Hassan"

    def test_valid_form_sets_submitted_flag(self, energies_placeholder):
        response = Client().post(
            "/energies/",
            {"name": "Test User", "email": "test@example.com"},
        )
        assert response.context["submitted"] is True

    def test_invalid_form_does_not_create_lead(self, energies_placeholder):
        count_before = Lead.objects.count()
        Client().post("/energies/", {"name": "", "email": "not-an-email"})
        assert Lead.objects.count() == count_before

    def test_form_vertical_set_from_url_not_input(self, energies_placeholder):
        Client().post(
            "/energies/",
            {
                "name": "Injector",
                "email": "injector@example.com",
                "vertical": "investments",
            },
        )
        lead = Lead.objects.filter(email="injector@example.com").first()
        assert lead is not None
        assert lead.vertical == "energies"


@pytest.mark.django_db
class TestTechnologiesRedirect:
    def test_technologies_path_redirects_permanent(self):
        response = Client().get("/technologies/")
        assert response.status_code == 301
        assert response["Location"] == "https://bjptechnologies.co.tz"
