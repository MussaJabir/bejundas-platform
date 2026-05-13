import pytest
from django.test import Client

from apps.leads.models import Lead, VerticalPlaceholder


@pytest.fixture
def financial_placeholder(db):
    # Seeded by migration — fetch the existing row
    return VerticalPlaceholder.objects.get(vertical="financial")


@pytest.mark.django_db
class TestComingSoonView:
    def test_known_vertical_returns_200(self, financial_placeholder):
        client = Client(SERVER_NAME="financial.bejundas.local")
        response = client.get("/")
        assert response.status_code == 200

    def test_uses_coming_soon_template(self, financial_placeholder):
        client = Client(SERVER_NAME="financial.bejundas.local")
        response = client.get("/")
        assert "leads/coming_soon.html" in [t.name for t in response.templates]

    def test_placeholder_in_context(self, financial_placeholder):
        client = Client(SERVER_NAME="financial.bejundas.local")
        response = client.get("/")
        assert response.context["placeholder"] == financial_placeholder

    def test_inactive_placeholder_not_shown(self, db):
        VerticalPlaceholder.objects.filter(vertical="farming").update(is_active=False)
        client = Client(SERVER_NAME="farming.bejundas.local")
        response = client.get("/")
        assert response.context["placeholder"] is None
        # restore
        VerticalPlaceholder.objects.filter(vertical="farming").update(is_active=True)

    def test_valid_form_creates_lead(self, financial_placeholder):
        client = Client(SERVER_NAME="financial.bejundas.local")
        client.post(
            "/",
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
        client = Client(SERVER_NAME="financial.bejundas.local")
        response = client.post(
            "/",
            {"name": "Test User", "email": "test@example.com"},
        )
        assert response.context["submitted"] is True

    def test_invalid_form_does_not_create_lead(self, financial_placeholder):
        client = Client(SERVER_NAME="financial.bejundas.local")
        count_before = Lead.objects.count()
        client.post("/", {"name": "", "email": "not-an-email"})
        assert Lead.objects.count() == count_before

    def test_form_vertical_set_from_host_not_input(self, financial_placeholder):
        client = Client(SERVER_NAME="financial.bejundas.local")
        client.post(
            "/",
            {
                "name": "Injector",
                "email": "injector@example.com",
                "vertical": "investments",
            },
        )
        lead = Lead.objects.filter(email="injector@example.com").first()
        assert lead is not None
        assert lead.vertical == "financial"
