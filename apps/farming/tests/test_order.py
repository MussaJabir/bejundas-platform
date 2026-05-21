"""Phase 4 — OrderInquiry form / view / email."""

import pytest
from django.test import Client

from apps.farming.forms import OrderInquiryForm, _validate_phone
from apps.farming.models import OrderInquiry

VALID_POST = {
    "full_name": "Asha Buyer",
    "organisation": "Asha Trading",
    "email": "asha@example.com",
    "phone": "+255712345678",
    "inquiry_type": "wholesale",
    "products_of_interest": "200 trays layer eggs weekly",
    "quantity": "200 trays",
    "frequency": "monthly",
    "delivery_location": "Dar es Salaam",
    "preferred_contact": "whatsapp",
    "notes": "Restaurant chain — supply Mon and Thu.",
}


class TestPhoneValidator:
    def test_accepts_nine_digits(self):
        assert _validate_phone("0712345678") == "0712345678"

    def test_accepts_country_prefix_with_punctuation(self):
        assert _validate_phone("+255 712 345 678") == "+255 712 345 678"

    def test_rejects_short_number(self):
        from django.core.exceptions import ValidationError

        with pytest.raises(ValidationError):
            _validate_phone("12345")

    def test_rejects_blank(self):
        from django.core.exceptions import ValidationError

        with pytest.raises(ValidationError):
            _validate_phone("")


@pytest.mark.django_db
class TestOrderInquiryFormValidation:
    def test_valid_form_is_valid(self):
        form = OrderInquiryForm(data=VALID_POST)
        assert form.is_valid(), form.errors

    def test_missing_required_fields_invalid(self):
        form = OrderInquiryForm(data={})
        assert not form.is_valid()
        for field in ["full_name", "email", "phone", "inquiry_type", "products_of_interest"]:
            assert field in form.errors

    def test_short_phone_rejected(self):
        bad = VALID_POST | {"phone": "12345"}
        form = OrderInquiryForm(data=bad)
        assert not form.is_valid()
        assert "phone" in form.errors

    def test_empty_products_rejected(self):
        bad = VALID_POST | {"products_of_interest": ""}
        form = OrderInquiryForm(data=bad)
        assert not form.is_valid()
        assert "products_of_interest" in form.errors

    def test_too_short_products_rejected(self):
        bad = VALID_POST | {"products_of_interest": "x"}
        form = OrderInquiryForm(data=bad)
        assert not form.is_valid()
        assert "products_of_interest" in form.errors


@pytest.mark.django_db
class TestOrderInquireView:
    def test_get_renders_form(self):
        response = Client().get("/farming/order/")
        assert response.status_code == 200
        assert "farming/order.html" in [t.name for t in response.templates]
        assert "form" in response.context

    def test_valid_post_creates_row(self):
        Client().post("/farming/order/", VALID_POST)
        row = OrderInquiry.objects.get(email="asha@example.com")
        assert row.full_name == "Asha Buyer"
        assert row.inquiry_type == "wholesale"
        assert row.status == "new"

    def test_valid_post_sends_email(self, mailoutbox):
        response = Client().post("/farming/order/", VALID_POST)
        assert response.status_code == 200
        assert response.context.get("sent") is True
        assert len(mailoutbox) == 1
        msg = mailoutbox[0]
        assert "Bejundas Farming Order" in msg.subject
        assert "Asha Trading" in msg.subject
        assert "Wholesale Buyer" in msg.subject
        # Plain-text body
        assert "Asha Buyer" in msg.body
        assert "200 trays layer eggs weekly" in msg.body
        # HTML alternative attached
        assert len(msg.alternatives) == 1
        html_body = msg.alternatives[0][0]
        assert "New Order Inquiry" in html_body
        assert "Bejundas Farming Ltd" in html_body

    def test_invalid_post_redisplays_form(self):
        bad = VALID_POST | {"email": "not-email"}
        response = Client().post("/farming/order/", bad)
        assert response.status_code == 200
        assert response.context["form"].errors
        # No row created
        assert OrderInquiry.objects.filter(email="not-email").count() == 0

    def test_email_failure_does_not_500(self, monkeypatch):
        """Per PR #55 — row saves, then email send raises, view should
        still render the success page (best-effort)."""

        def boom(self, request=None):
            raise RuntimeError("SMTP down")

        from apps.farming import forms as farming_forms

        monkeypatch.setattr(farming_forms.OrderInquiryForm, "send_notification", boom)
        response = Client().post("/farming/order/", VALID_POST)
        assert response.status_code == 200
        assert response.context.get("sent") is True
        # Row should still have been saved before the email blew up.
        assert OrderInquiry.objects.filter(email="asha@example.com").exists()


@pytest.mark.django_db
class TestSitemapIncludesOrder:
    def test_sitemap_includes_order_url(self):
        response = Client().get("/sitemap.xml")
        assert response.status_code == 200
        assert "/farming/order/" in response.content.decode()


@pytest.mark.django_db
class TestNavbarHasOrderLink:
    def test_navbar_has_place_an_order_link(self):
        response = Client().get("/farming/")
        body = response.content.decode()
        assert "Place an Order" in body
        assert 'href="/farming/order/"' in body
