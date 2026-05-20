from decimal import Decimal

import pytest
from django.test import Client
from django.urls import NoReverseMatch, resolve, reverse

from apps.financial.models import FinancialService, InvestmentOffering


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


@pytest.mark.django_db
class TestInnerPages:
    """Phase 3 — about / services / investments / contact render 200 with the right template."""

    @pytest.mark.parametrize(
        "url,template",
        [
            ("/financial/about/", "financial/about.html"),
            ("/financial/services/", "financial/services.html"),
            ("/financial/investments/", "financial/investments.html"),
            ("/financial/contact/", "financial/contact.html"),
        ],
    )
    def test_inner_page_loads(self, url, template):
        response = Client().get(url)
        assert response.status_code == 200
        assert template in [t.name for t in response.templates]

    def test_investment_detail_loads(self):
        offering = InvestmentOffering.objects.create(
            reference_id="TEST/IO/2026/DETAIL",
            title="Test Detail Round",
            tenure_months=12,
            indicative_rate_pct=Decimal("16.50"),
            min_capital=Decimal("250000.00"),
        )
        response = Client().get(f"/financial/investments/{offering.slug}/")
        assert response.status_code == 200
        assert "financial/investment_detail.html" in [t.name for t in response.templates]
        assert b"Test Detail Round" in response.content

    def test_investment_detail_404_for_unknown_slug(self):
        response = Client().get("/financial/investments/does-not-exist/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestServicesCategoryFilter:
    """Category filter narrows the queryset deterministically."""

    def setup_method(self, method):
        FinancialService.objects.all().delete()
        FinancialService.objects.create(name="Personal Loan", category="loans", summary="x")
        FinancialService.objects.create(name="SME Loan", category="loans", summary="x")
        FinancialService.objects.create(name="T-Bills", category="securities", summary="x")

    def test_all_categories_shown_by_default(self):
        response = Client().get("/financial/services/")
        assert len(response.context["services"]) == 3
        assert response.context["active_category"] == ""

    def test_filter_loans_narrows_queryset(self):
        response = Client().get("/financial/services/?category=loans")
        assert len(response.context["services"]) == 2
        assert response.context["active_category"] == "loans"
        for s in response.context["services"]:
            assert s.category == "loans"

    def test_filter_securities_narrows_queryset(self):
        response = Client().get("/financial/services/?category=securities")
        assert len(response.context["services"]) == 1
        assert response.context["services"][0].name == "T-Bills"

    def test_unknown_category_falls_back_to_all(self):
        response = Client().get("/financial/services/?category=garbage")
        assert len(response.context["services"]) == 3
        assert response.context["active_category"] == ""


@pytest.mark.django_db
class TestInvestmentsStatusFilter:
    """Investments list filter narrows by status deterministically."""

    def setup_method(self, method):
        InvestmentOffering.objects.all().delete()
        for ref, status in [
            ("TEST/IO/2026/A", "open"),
            ("TEST/IO/2026/B", "open"),
            ("TEST/IO/2026/C", "upcoming"),
            ("TEST/IO/2026/D", "closed"),
        ]:
            InvestmentOffering.objects.create(
                reference_id=ref,
                title=ref,
                tenure_months=12,
                indicative_rate_pct=Decimal("16.50"),
                min_capital=Decimal("250000.00"),
                status=status,
            )

    def test_all_offerings_shown_by_default(self):
        response = Client().get("/financial/investments/")
        assert len(response.context["offerings"]) == 4
        assert response.context["active_status"] == ""

    def test_filter_open_narrows_queryset(self):
        response = Client().get("/financial/investments/?status=open")
        assert len(response.context["offerings"]) == 2
        assert response.context["active_status"] == "open"

    def test_filter_upcoming_narrows_queryset(self):
        response = Client().get("/financial/investments/?status=upcoming")
        assert len(response.context["offerings"]) == 1

    def test_unknown_status_falls_back_to_all(self):
        response = Client().get("/financial/investments/?status=garbage")
        assert len(response.context["offerings"]) == 4
        assert response.context["active_status"] == ""


@pytest.mark.django_db
class TestContactForm:
    def test_get_renders_empty_form(self):
        response = Client().get("/financial/contact/")
        assert response.status_code == 200
        assert "form" in response.context

    def test_post_invalid_redisplays_form(self):
        response = Client().post("/financial/contact/", {"name": "", "email": "not-email"})
        assert response.status_code == 200
        assert response.context["form"].errors

    def test_post_valid_sends_email(self, mailoutbox):
        response = Client().post(
            "/financial/contact/",
            {
                "name": "Amina Hassan",
                "email": "amina@example.com",
                "phone": "+255712345678",
                "subject": "Investment query",
                "message": "I would like to learn more about the 2-year round.",
            },
        )
        assert response.status_code == 200
        assert response.context.get("sent") is True
        assert len(mailoutbox) == 1
        msg = mailoutbox[0]
        assert "Investment query" in msg.subject
        assert "Amina Hassan" in msg.body
        assert "+255712345678" in msg.body


@pytest.mark.django_db
class TestFinancialSitemap:
    def test_sitemap_includes_financial_pages(self):
        response = Client().get("/sitemap.xml")
        assert response.status_code == 200
        body = response.content.decode()
        assert "/financial/" in body
        assert "/financial/about/" in body
        assert "/financial/services/" in body
        assert "/financial/investments/" in body
        assert "/financial/contact/" in body

    def test_sitemap_includes_offering_detail_urls(self):
        InvestmentOffering.objects.create(
            reference_id="TEST/IO/SITEMAP/01",
            title="Sitemap Round",
            tenure_months=12,
            indicative_rate_pct=Decimal("16.50"),
            min_capital=Decimal("250000.00"),
        )
        response = Client().get("/sitemap.xml")
        assert "/financial/investments/test-io-sitemap-01/" in response.content.decode()
