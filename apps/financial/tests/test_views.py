import pytest
from django.test import Client
from django.urls import NoReverseMatch, resolve, reverse


@pytest.mark.django_db
class TestFinancialHomeView:
    def test_home_returns_200(self):
        response = Client().get("/financial/")
        assert response.status_code == 200

    def test_home_uses_financial_template(self):
        response = Client().get("/financial/")
        assert "financial/home.html" in [t.name for t in response.templates]

    def test_home_url_resolves_to_financial_app(self):
        match = resolve("/financial/")
        assert match.app_name == "financial"
        assert match.url_name == "home"

    def test_home_reverse_lookup(self):
        assert reverse("financial:home") == "/financial/"

    def test_app_theme_is_financial_navy_gold(self):
        response = Client().get("/financial/")
        theme = response.context["app_theme"]
        assert theme["primary"] == "#0a2342"
        assert theme["accent"] == "#c9a84c"
        assert theme["label"] == "Financial Services"
        assert theme["legal_name"] == "BEJUNDAS FINANCIAL SERVICES LTD"


@pytest.mark.django_db
class TestRoutingHandoff:
    def test_leads_financial_url_no_longer_resolves(self):
        """Phase 1 removed the financial Coming Soon route from apps.leads."""
        with pytest.raises(NoReverseMatch):
            reverse("leads:financial")

    def test_other_coming_soon_routes_still_resolve(self):
        """Sanity — energies/farming/investments are still in apps.leads."""
        assert reverse("leads:energies") == "/energies/"
        assert reverse("leads:farming") == "/farming/"
        assert reverse("leads:investments") == "/investments/"


@pytest.mark.django_db
class TestNavbarAndDisclaimer:
    def test_navbar_shows_bfs_legal_entity_split(self):
        response = Client().get("/financial/")
        body = response.content.decode()
        assert "BEJUNDAS FINANCIAL" in body
        assert "SERVICES LTD" in body

    def test_navbar_aria_label_is_full_legal_name(self):
        response = Client().get("/financial/")
        body = response.content.decode()
        assert 'aria-label="BEJUNDAS FINANCIAL SERVICES LTD"' in body

    def test_footer_copyright_uses_bfs_legal_entity(self):
        response = Client().get("/financial/")
        body = response.content.decode()
        assert "BEJUNDAS FINANCIAL SERVICES LTD" in body

    def test_regulatory_disclaimer_present(self):
        response = Client().get("/financial/")
        body = response.content.decode()
        assert "Regulatory notice" in body
        assert "private placements" in body
        assert "not deposits" in body
        assert "Capital Markets and Securities Authority" in body

    def test_values_triad_present(self):
        response = Client().get("/financial/")
        body = response.content.decode()
        assert "Salama" in body
        assert "Faida" in body
        assert "Uaminifu" in body
