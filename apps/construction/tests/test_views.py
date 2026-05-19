import pytest
from django.test import Client
from django.urls import resolve, reverse


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
        from django.urls import NoReverseMatch

        with pytest.raises(NoReverseMatch):
            reverse("leads:construction")
