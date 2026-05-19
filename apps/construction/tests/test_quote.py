"""Phase 4 — QuoteRequest model, form validation, view, email + admin action tests."""

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse

from apps.construction.forms import QuoteRequestForm
from apps.construction.models import QuoteAttachment, QuoteRequest

# ── Helpers ─────────────────────────────────────────────────────────


def _valid_payload(**overrides):
    payload = {
        "full_name": "Amina Hassan",
        "company": "Hassan Holdings Ltd",
        "email": "amina@example.com",
        "phone": "+255712345678",
        "project_type": "residential",
        "location_region": "Dar es Salaam",
        "location_district": "Masaki",
        "estimated_start": "2026-08-01",
        "scope_description": (
            "Four-bedroom villa on a 600 sqm plot. Three storeys plus rooftop terrace. "
            "Need full design-build including MEP and landscaping."
        ),
        "budget_range": "200m_1b",
        "timeline": "6_12",
    }
    payload.update(overrides)
    return payload


def _make_file(name="plan.pdf", size=1024, content_type="application/pdf"):
    return SimpleUploadedFile(name, b"x" * size, content_type=content_type)


# ── Model tests ─────────────────────────────────────────────────────


@pytest.mark.django_db
class TestQuoteRequestModel:
    def test_default_status_is_new(self):
        q = QuoteRequest.objects.create(
            full_name="X",
            email="x@example.com",
            phone="+255700000000",
            project_type="commercial",
            location_region="Arusha",
            scope_description="x" * 60,
            budget_range="50m_200m",
            timeline="3_6",
        )
        assert q.status == "new"

    def test_str_uses_company_when_present(self):
        q = QuoteRequest.objects.create(
            full_name="John",
            company="Acme Ltd",
            email="j@example.com",
            phone="+255700000000",
            project_type="commercial",
            location_region="Dar",
            scope_description="x" * 60,
            budget_range="50m_200m",
            timeline="3_6",
        )
        assert "Acme Ltd" in str(q)
        assert "Commercial" in str(q)

    def test_str_falls_back_to_full_name(self):
        q = QuoteRequest.objects.create(
            full_name="Solo Person",
            email="s@example.com",
            phone="+255700000000",
            project_type="renovation",
            location_region="Mwanza",
            scope_description="x" * 60,
            budget_range="under_50m",
            timeline="1_3",
        )
        assert "Solo Person" in str(q)


# ── Form validation tests ───────────────────────────────────────────


@pytest.mark.django_db
class TestQuoteRequestForm:
    def test_valid_form(self):
        form = QuoteRequestForm(data=_valid_payload())
        assert form.is_valid(), form.errors

    def test_scope_too_short_rejected(self):
        form = QuoteRequestForm(data=_valid_payload(scope_description="too short"))
        assert not form.is_valid()
        assert "scope_description" in form.errors

    def test_required_fields_enforced(self):
        form = QuoteRequestForm(data={})
        assert not form.is_valid()
        for field in [
            "full_name",
            "email",
            "phone",
            "project_type",
            "location_region",
            "scope_description",
            "budget_range",
            "timeline",
        ]:
            assert field in form.errors

    def test_company_is_optional(self):
        form = QuoteRequestForm(data=_valid_payload(company=""))
        assert form.is_valid(), form.errors

    def test_attachment_too_large_rejected(self):
        big = _make_file(name="big.pdf", size=6 * 1024 * 1024)
        form = QuoteRequestForm(data=_valid_payload(), files={"attachment_1": big})
        assert not form.is_valid()
        assert "attachment_1" in form.errors

    def test_attachment_wrong_extension_rejected(self):
        evil = _make_file(name="hack.exe", size=512, content_type="application/octet-stream")
        form = QuoteRequestForm(data=_valid_payload(), files={"attachment_1": evil})
        assert not form.is_valid()
        assert "attachment_1" in form.errors

    def test_valid_pdf_accepted(self):
        f = _make_file(name="plan.pdf", size=1024)
        form = QuoteRequestForm(data=_valid_payload(), files={"attachment_1": f})
        assert form.is_valid(), form.errors


# ── View tests ──────────────────────────────────────────────────────


@pytest.mark.django_db
class TestQuoteRequestView:
    def test_get_returns_200(self):
        response = Client().get("/construction/quote/")
        assert response.status_code == 200
        assert "construction/quote_request.html" in [t.name for t in response.templates]

    def test_get_renders_empty_form(self):
        response = Client().get("/construction/quote/")
        assert "form" in response.context

    def test_post_valid_creates_record(self):
        Client().post("/construction/quote/", _valid_payload())
        assert QuoteRequest.objects.count() == 1
        q = QuoteRequest.objects.first()
        assert q.full_name == "Amina Hassan"
        assert q.status == "new"

    def test_post_valid_sends_email(self, mailoutbox):
        Client().post("/construction/quote/", _valid_payload())
        assert len(mailoutbox) == 1
        msg = mailoutbox[0]
        assert "Bejundas Construction RFP" in msg.subject
        assert "Hassan Holdings Ltd" in msg.subject
        assert "Amina Hassan" in msg.body

    def test_post_valid_shows_success(self):
        response = Client().post("/construction/quote/", _valid_payload())
        assert response.status_code == 200
        assert response.context.get("sent") is True

    def test_post_invalid_redisplays_errors(self):
        response = Client().post("/construction/quote/", {})
        assert response.status_code == 200
        assert response.context["form"].errors

    def test_post_with_attachment_creates_attachment(self, tmp_path, settings):
        settings.MEDIA_ROOT = tmp_path
        f = _make_file(name="plan.pdf", size=1024)
        Client().post("/construction/quote/", {**_valid_payload(), "attachment_1": f})
        assert QuoteAttachment.objects.count() == 1
        att = QuoteAttachment.objects.first()
        assert "plan" in att.file.name


# ── Admin action tests ──────────────────────────────────────────────


@pytest.fixture
def admin_client(db):
    User = get_user_model()
    user = User.objects.create_user(
        username="admin", password="testpass", is_staff=True, is_superuser=True
    )
    c = Client()
    c.force_login(user)
    return c


@pytest.mark.django_db
class TestQuoteRequestAdmin:
    def _make_quote(self):
        return QuoteRequest.objects.create(
            full_name="Test",
            email="t@example.com",
            phone="+255700000000",
            project_type="residential",
            location_region="Dar",
            scope_description="x" * 60,
            budget_range="50m_200m",
            timeline="3_6",
        )

    def test_changelist_loads(self, admin_client):
        q = self._make_quote()
        response = admin_client.get(reverse("admin:construction_quoterequest_changelist"))
        assert response.status_code == 200
        assert q.full_name.encode() in response.content

    def test_mark_as_reviewed_action(self, admin_client):
        q = self._make_quote()
        admin_client.post(
            reverse("admin:construction_quoterequest_changelist"),
            {
                "action": "mark_as_reviewed",
                "_selected_action": [str(q.pk)],
            },
        )
        q.refresh_from_db()
        assert q.status == "reviewed"

    def test_mark_as_won_action(self, admin_client):
        q = self._make_quote()
        admin_client.post(
            reverse("admin:construction_quoterequest_changelist"),
            {
                "action": "mark_as_won",
                "_selected_action": [str(q.pk)],
            },
        )
        q.refresh_from_db()
        assert q.status == "won"

    def test_mark_as_lost_action(self, admin_client):
        q = self._make_quote()
        admin_client.post(
            reverse("admin:construction_quoterequest_changelist"),
            {
                "action": "mark_as_lost",
                "_selected_action": [str(q.pk)],
            },
        )
        q.refresh_from_db()
        assert q.status == "lost"
