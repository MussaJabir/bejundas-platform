import pytest
from django.test import Client

from apps.leads.models import Lead, VerticalPlaceholder


@pytest.fixture
def financial_placeholder(db):
    return VerticalPlaceholder.objects.get(vertical="financial")


@pytest.mark.django_db
class TestComingSoonView:
    def test_known_vertical_returns_200(self, financial_placeholder):
        response = Client().get("/financial/")
        assert response.status_code == 200

    def test_uses_coming_soon_template(self, financial_placeholder):
        response = Client().get("/financial/")
        assert "leads/coming_soon.html" in [t.name for t in response.templates]

    def test_placeholder_in_context(self, financial_placeholder):
        response = Client().get("/financial/")
        assert response.context["placeholder"] == financial_placeholder

    def test_inactive_placeholder_not_shown(self, db):
        VerticalPlaceholder.objects.filter(vertical="farming").update(is_active=False)
        try:
            response = Client().get("/farming/")
            assert response.context["placeholder"] is None
        finally:
            VerticalPlaceholder.objects.filter(vertical="farming").update(is_active=True)

    def test_valid_form_creates_lead(self, financial_placeholder):
        Client().post(
            "/financial/",
            {
                "name": "Amina Hassan",
                "email": "amina@example.com",
                "phone": "+255712345678",
                "message": "Interested in your services.",
            },
        )
        lead = Lead.objects.get(email="amina@example.com")
        assert lead.vertical == "financial"
        assert lead.name == "Amina Hassan"

    def test_valid_form_sets_submitted_flag(self, financial_placeholder):
        response = Client().post(
            "/financial/",
            {"name": "Test User", "email": "test@example.com"},
        )
        assert response.context["submitted"] is True

    def test_invalid_form_does_not_create_lead(self, financial_placeholder):
        count_before = Lead.objects.count()
        Client().post("/financial/", {"name": "", "email": "not-an-email"})
        assert Lead.objects.count() == count_before

    def test_form_vertical_set_from_url_not_input(self, financial_placeholder):
        Client().post(
            "/financial/",
            {
                "name": "Injector",
                "email": "injector@example.com",
                "vertical": "investments",
            },
        )
        lead = Lead.objects.filter(email="injector@example.com").first()
        assert lead is not None
        assert lead.vertical == "financial"


@pytest.mark.django_db
class TestTechnologiesRedirect:
    def test_technologies_path_redirects_permanent(self):
        response = Client().get("/technologies/")
        assert response.status_code == 301
        assert response["Location"] == "https://bjptechnologies.co.tz"
