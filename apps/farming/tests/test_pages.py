"""Phase 3 — about / products / farms / contact render 200 with the right
template and respect filters."""

import pytest
from django.test import Client

from apps.farming.models import Farm, FarmingProduct


@pytest.mark.django_db
class TestInnerPagesLoad:
    @pytest.mark.parametrize(
        "url,template",
        [
            ("/farming/about/", "farming/about.html"),
            ("/farming/products/", "farming/products.html"),
            ("/farming/farms/", "farming/farms.html"),
            ("/farming/contact/", "farming/contact.html"),
        ],
    )
    def test_inner_page_loads(self, url, template):
        response = Client().get(url)
        assert response.status_code == 200
        assert template in [t.name for t in response.templates]


@pytest.mark.django_db
class TestProductsCategoryFilter:
    def setup_method(self, method):
        FarmingProduct.objects.all().delete()
        FarmingProduct.objects.create(name="Maize", category="crops", summary="x")
        FarmingProduct.objects.create(name="Beans", category="crops", summary="x")
        FarmingProduct.objects.create(name="Layer Eggs", category="poultry", summary="x")
        FarmingProduct.objects.create(name="Sunflower Oil", category="processed", summary="x")

    def test_all_products_shown_by_default(self):
        response = Client().get("/farming/products/")
        assert len(response.context["products"]) == 4
        assert response.context["active_category"] == ""

    def test_filter_crops_narrows_queryset(self):
        response = Client().get("/farming/products/?category=crops")
        assert len(response.context["products"]) == 2
        assert response.context["active_category"] == "crops"
        for p in response.context["products"]:
            assert p.category == "crops"

    def test_filter_poultry_narrows_queryset(self):
        response = Client().get("/farming/products/?category=poultry")
        assert len(response.context["products"]) == 1

    def test_unknown_category_falls_back_to_all(self):
        response = Client().get("/farming/products/?category=garbage")
        assert len(response.context["products"]) == 4
        assert response.context["active_category"] == ""

    def test_inactive_products_excluded(self):
        FarmingProduct.objects.filter(name="Maize").update(is_active=False)
        response = Client().get("/farming/products/")
        assert len(response.context["products"]) == 3


@pytest.mark.django_db
class TestFarmsList:
    def test_farms_in_context(self):
        Farm.objects.create(name="Mbeya Farm", region="Mbeya", primary_activity="crops")
        Farm.objects.create(name="Coast Farm", region="Pwani", primary_activity="poultry")
        response = Client().get("/farming/farms/")
        assert response.context["farms"].count() == 2

    def test_empty_state_message_when_no_farms(self):
        Farm.objects.all().delete()
        response = Client().get("/farming/farms/")
        body = response.content.decode()
        assert "being added to the admin" in body


@pytest.mark.django_db
class TestContactForm:
    def test_get_renders_empty_form(self):
        response = Client().get("/farming/contact/")
        assert response.status_code == 200
        assert "form" in response.context

    def test_post_invalid_redisplays_form(self):
        response = Client().post("/farming/contact/", {"name": "", "email": "not-email"})
        assert response.status_code == 200
        assert response.context["form"].errors

    def test_post_valid_sends_email(self, mailoutbox):
        response = Client().post(
            "/farming/contact/",
            {
                "name": "Asha Buyer",
                "email": "asha@example.com",
                "phone": "+255712345678",
                "subject": "Wholesale eggs",
                "message": "We're a Dar restaurant chain — looking for 50 trays weekly.",
            },
        )
        assert response.status_code == 200
        assert response.context.get("sent") is True
        assert len(mailoutbox) == 1
        msg = mailoutbox[0]
        assert "Wholesale eggs" in msg.subject
        assert "Asha Buyer" in msg.body
        assert "+255712345678" in msg.body

    def test_email_failure_still_shows_success(self, monkeypatch):
        """Per PR #55 — SMTP failures must not 500 the visitor."""

        def boom(*args, **kwargs):
            raise RuntimeError("SMTP down")

        from apps.farming import forms as farming_forms

        monkeypatch.setattr(farming_forms.ContactForm, "send_email", boom)
        response = Client().post(
            "/farming/contact/",
            {
                "name": "Asha",
                "email": "a@b.com",
                "phone": "0712345678",
                "subject": "Test",
                "message": "Test message.",
            },
        )
        assert response.status_code == 200
        assert response.context.get("sent") is True


@pytest.mark.django_db
class TestSitemapExtended:
    def test_sitemap_includes_all_farming_pages(self):
        response = Client().get("/sitemap.xml")
        assert response.status_code == 200
        body = response.content.decode()
        for path in [
            "/farming/",
            "/farming/about/",
            "/farming/products/",
            "/farming/farms/",
            "/farming/contact/",
        ]:
            assert path in body


@pytest.mark.django_db
class TestHomeWiresDB:
    def test_home_pulls_featured_products(self):
        FarmingProduct.objects.create(
            name="Featured Maize", category="crops", summary="x", is_featured=True
        )
        FarmingProduct.objects.create(
            name="Hidden Beans", category="crops", summary="x", is_featured=False
        )
        response = Client().get("/farming/")
        names = [p.name for p in response.context["featured_products"]]
        assert "Featured Maize" in names
        assert "Hidden Beans" not in names

    def test_home_pulls_farms(self):
        Farm.objects.create(name="Mbeya Farm", region="Mbeya", primary_activity="crops")
        response = Client().get("/farming/")
        assert response.context["featured_farms"].count() == 1
