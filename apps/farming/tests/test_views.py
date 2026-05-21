import pytest
from django.test import Client
from django.urls import NoReverseMatch, resolve, reverse


@pytest.mark.django_db
class TestFarmingHomeView:
    def test_home_returns_200(self):
        response = Client().get("/farming/")
        assert response.status_code == 200

    def test_home_uses_farming_template(self):
        response = Client().get("/farming/")
        assert "farming/home.html" in [t.name for t in response.templates]

    def test_home_url_resolves_to_farming_app(self):
        match = resolve("/farming/")
        assert match.app_name == "farming"
        assert match.url_name == "home"

    def test_home_reverse_lookup(self):
        assert reverse("farming:home") == "/farming/"

    def test_app_theme_is_farming_forest_lime(self):
        response = Client().get("/farming/")
        theme = response.context["app_theme"]
        assert theme["primary"] == "#2d5a27"
        assert theme["accent"] == "#8bc34a"
        assert theme["label"] == "Farming"
        assert theme["legal_name"] == "BEJUNDAS FARMING LTD"


@pytest.mark.django_db
class TestRoutingHandoff:
    def test_leads_farming_url_no_longer_resolves(self):
        """Phase 1 removed the farming Coming Soon route from apps.leads."""
        with pytest.raises(NoReverseMatch):
            reverse("leads:farming")

    def test_other_coming_soon_routes_still_resolve(self):
        """Sanity — energies and investments are still in apps.leads."""
        assert reverse("leads:energies") == "/energies/"
        assert reverse("leads:investments") == "/investments/"


@pytest.mark.django_db
class TestNavbarAndContent:
    def test_navbar_shows_bfl_legal_entity_split(self):
        response = Client().get("/farming/")
        body = response.content.decode()
        assert "BEJUNDAS FARMING" in body
        assert "LTD" in body

    def test_navbar_aria_label_is_full_legal_name(self):
        response = Client().get("/farming/")
        body = response.content.decode()
        assert 'aria-label="BEJUNDAS FARMING LTD"' in body

    def test_footer_copyright_uses_bfl_legal_entity(self):
        response = Client().get("/farming/")
        body = response.content.decode()
        assert "BEJUNDAS FARMING LTD" in body

    def test_values_triad_present(self):
        response = Client().get("/farming/")
        body = response.content.decode()
        assert "Asili" in body
        assert "Ubora" in body
        assert "Uaminifu" in body

    def test_back_link_to_bejundas_group(self):
        response = Client().get("/farming/")
        body = response.content.decode()
        assert "Bejundas Group" in body

    def test_home_cta_points_at_contact_form(self):
        """Phase 3 swapped the placeholder WhatsApp CTA for the new
        /farming/contact/ form."""
        response = Client().get("/farming/")
        body = response.content.decode()
        assert "/farming/contact/" in body


@pytest.mark.django_db
class TestFarmingSitemap:
    def test_sitemap_includes_farming_home(self):
        response = Client().get("/sitemap.xml")
        assert response.status_code == 200
        assert "/farming/" in response.content.decode()

    def test_hub_sitemap_no_longer_references_leads_farming(self):
        """Belt-and-braces — hub sitemap STATIC_PAGES dropped the leads:farming row."""
        from apps.hub.sitemaps import STATIC_PAGES

        names = [p[0] for p in STATIC_PAGES]
        assert "leads:farming" not in names
