import pytest
from django.test import Client
from django.urls import NoReverseMatch, resolve, reverse

from apps.construction.models import Project


@pytest.mark.django_db
class TestConstructionHomeView:
    def test_home_returns_200(self):
        response = Client().get("/construction/")
        assert response.status_code == 200

    def test_home_uses_construction_template(self):
        response = Client().get("/construction/")
        assert "construction/home.html" in [t.name for t in response.templates]

    def test_home_url_resolves_to_construction_app(self):
        match = resolve("/construction/")
        assert match.app_name == "construction"
        assert match.url_name == "home"

    def test_home_reverse_lookup(self):
        assert reverse("construction:home") == "/construction/"

    def test_app_theme_is_construction(self):
        response = Client().get("/construction/")
        theme = response.context["app_theme"]
        assert theme["primary"] == "#2c2c2c"
        assert theme["accent"] == "#f47920"
        assert theme["label"] == "Construction"


@pytest.mark.django_db
class TestRoutingHandoff:
    def test_leads_construction_url_no_longer_resolves(self):
        """The old apps.leads route for construction was removed in Phase 1."""
        with pytest.raises(NoReverseMatch):
            reverse("leads:construction")


@pytest.mark.django_db
class TestInnerPages:
    """Phase 3 — 5 inner pages render 200 with the right template."""

    @pytest.mark.parametrize(
        "url,template",
        [
            ("/construction/about/", "construction/about.html"),
            ("/construction/services/", "construction/services.html"),
            ("/construction/projects/", "construction/projects.html"),
            ("/construction/contact/", "construction/contact.html"),
        ],
    )
    def test_inner_page_loads(self, url, template):
        response = Client().get(url)
        assert response.status_code == 200
        assert template in [t.name for t in response.templates]

    def test_project_detail_loads(self):
        project = Project.objects.create(
            title="Test Tower",
            sector="residential",
            location_city="Dar",
            year_completed=2024,
        )
        response = Client().get(f"/construction/projects/{project.slug}/")
        assert response.status_code == 200
        assert "construction/project_detail.html" in [t.name for t in response.templates]
        assert b"Test Tower" in response.content

    def test_project_detail_404_for_unknown_slug(self):
        response = Client().get("/construction/projects/does-not-exist/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestProjectsSectorFilter:
    def setup_method(self, method):
        Project.objects.create(
            title="House A", sector="residential", location_city="Dar", year_completed=2024
        )
        Project.objects.create(
            title="House B", sector="residential", location_city="Arusha", year_completed=2023
        )
        Project.objects.create(
            title="Road A", sector="civil", location_city="Mwanza", year_completed=2022
        )

    def test_all_sectors_shown_by_default(self):
        response = Client().get("/construction/projects/")
        assert len(response.context["projects"]) == 3
        assert response.context["active_sector"] == ""

    def test_filter_residential_narrows_queryset(self):
        response = Client().get("/construction/projects/?sector=residential")
        assert len(response.context["projects"]) == 2
        assert response.context["active_sector"] == "residential"
        for p in response.context["projects"]:
            assert p.sector == "residential"

    def test_filter_civil_narrows_queryset(self):
        response = Client().get("/construction/projects/?sector=civil")
        assert len(response.context["projects"]) == 1
        assert response.context["projects"][0].title == "Road A"

    def test_unknown_sector_falls_back_to_all(self):
        response = Client().get("/construction/projects/?sector=garbage")
        assert len(response.context["projects"]) == 3
        assert response.context["active_sector"] == ""


@pytest.mark.django_db
class TestContactForm:
    def test_get_renders_empty_form(self):
        response = Client().get("/construction/contact/")
        assert response.status_code == 200
        assert "form" in response.context

    def test_post_invalid_redisplays_form(self):
        response = Client().post("/construction/contact/", {"name": "", "email": "not-email"})
        assert response.status_code == 200
        assert response.context["form"].errors

    def test_post_valid_sends_email(self, mailoutbox):
        response = Client().post(
            "/construction/contact/",
            {
                "name": "Amina Hassan",
                "email": "amina@example.com",
                "phone": "+255712345678",
                "subject": "Site visit request",
                "message": "We have a plot in Masaki and would like a meeting.",
            },
        )
        assert response.status_code == 200
        assert response.context.get("sent") is True
        assert len(mailoutbox) == 1
        msg = mailoutbox[0]
        assert "Site visit request" in msg.subject
        assert "Amina Hassan" in msg.body
        assert "+255712345678" in msg.body


@pytest.mark.django_db
class TestConstructionSitemap:
    def test_sitemap_includes_construction_pages(self):
        response = Client().get("/sitemap.xml")
        assert response.status_code == 200
        body = response.content.decode()
        assert "/construction/" in body
        assert "/construction/about/" in body
        assert "/construction/services/" in body
        assert "/construction/projects/" in body
        assert "/construction/contact/" in body

    def test_sitemap_includes_project_detail_urls(self):
        Project.objects.create(
            title="Sitemap Test", sector="residential", location_city="Dar", year_completed=2025
        )
        response = Client().get("/sitemap.xml")
        assert "/construction/projects/sitemap-test/" in response.content.decode()
