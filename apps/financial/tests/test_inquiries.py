"""Phase 4 — LoanInquiry + InvestmentInquiry forms + views + email."""

from decimal import Decimal

import pytest
from django.test import Client

from apps.financial.forms import InvestmentInquiryForm, LoanInquiryForm
from apps.financial.models import InvestmentInquiry, InvestmentOffering, LoanInquiry

# ── Form-level tests ────────────────────────────────────────────────


def _loan_payload(**overrides):
    payload = {
        "full_name": "Amina Hassan",
        "business_name": "Amina Trading",
        "email": "amina@example.com",
        "phone": "+255712345678",
        "loan_purpose": "sme",
        "amount_requested": "5000000",
        "tenure_band": "12_24",
        "preferred_contact": "phone",
        "notes": "We are expanding the kiosk into a second location.",
    }
    payload.update(overrides)
    return payload


def _investment_payload(**overrides):
    payload = {
        "full_name": "Fatma Investor",
        "email": "fatma@example.com",
        "phone": "+255712345678",
        "capital_band": "1m_5m",
        "preferred_tenure": "2yr",
        "funding_source": "savings",
        "preferred_contact": "whatsapp",
        "notes": "Looking to allocate over the next quarter.",
    }
    payload.update(overrides)
    return payload


@pytest.mark.django_db
class TestLoanInquiryForm:
    def test_valid_data(self):
        form = LoanInquiryForm(data=_loan_payload())
        assert form.is_valid(), form.errors

    def test_missing_required_fields(self):
        form = LoanInquiryForm(data={})
        assert not form.is_valid()
        for field in [
            "full_name",
            "email",
            "phone",
            "loan_purpose",
            "amount_requested",
            "tenure_band",
        ]:
            assert field in form.errors

    def test_amount_must_be_positive(self):
        form = LoanInquiryForm(data=_loan_payload(amount_requested="0"))
        assert not form.is_valid()
        assert "amount_requested" in form.errors

    def test_amount_negative_rejected(self):
        form = LoanInquiryForm(data=_loan_payload(amount_requested="-100"))
        assert not form.is_valid()
        assert "amount_requested" in form.errors

    def test_phone_too_short_rejected(self):
        form = LoanInquiryForm(data=_loan_payload(phone="123"))
        assert not form.is_valid()
        assert "phone" in form.errors

    def test_invalid_email_rejected(self):
        form = LoanInquiryForm(data=_loan_payload(email="not-an-email"))
        assert not form.is_valid()
        assert "email" in form.errors

    def test_business_name_optional(self):
        form = LoanInquiryForm(data=_loan_payload(business_name=""))
        assert form.is_valid(), form.errors

    def test_notes_optional(self):
        form = LoanInquiryForm(data=_loan_payload(notes=""))
        assert form.is_valid(), form.errors


@pytest.mark.django_db
class TestInvestmentInquiryForm:
    def test_valid_data(self):
        form = InvestmentInquiryForm(data=_investment_payload())
        assert form.is_valid(), form.errors

    def test_missing_required_fields(self):
        form = InvestmentInquiryForm(data={})
        assert not form.is_valid()
        for field in ["full_name", "email", "phone", "capital_band"]:
            assert field in form.errors

    def test_phone_too_short_rejected(self):
        form = InvestmentInquiryForm(data=_investment_payload(phone="abc"))
        assert not form.is_valid()
        assert "phone" in form.errors

    def test_notes_optional(self):
        form = InvestmentInquiryForm(data=_investment_payload(notes=""))
        assert form.is_valid(), form.errors


# ── View + email tests ──────────────────────────────────────────────


@pytest.mark.django_db
class TestLoanApplyView:
    def test_get_renders_empty_form(self):
        response = Client().get("/financial/loans/apply/")
        assert response.status_code == 200
        assert "form" in response.context
        assert "financial/loan_apply.html" in [t.name for t in response.templates]

    def test_post_invalid_redisplays_form(self):
        response = Client().post(
            "/financial/loans/apply/",
            {"full_name": "", "email": "not-an-email"},
        )
        assert response.status_code == 200
        assert response.context["form"].errors

    def test_post_valid_creates_row_and_sends_email(self, mailoutbox):
        response = Client().post("/financial/loans/apply/", _loan_payload())
        assert response.status_code == 200
        assert response.context.get("sent") is True

        # Row created
        loan = LoanInquiry.objects.get(email="amina@example.com")
        assert loan.full_name == "Amina Hassan"
        assert loan.business_name == "Amina Trading"
        assert loan.amount_requested == Decimal("5000000.00")
        assert loan.loan_purpose == "sme"
        assert loan.status == "new"

        # Email dispatched
        assert len(mailoutbox) == 1
        msg = mailoutbox[0]
        assert "Loan Inquiry" in msg.subject
        assert "Amina Trading" in msg.subject
        assert "Amina Hassan" in msg.body
        assert "TZS 5,000,000" in msg.body
        # HTML alternative attached
        assert len(msg.alternatives) == 1
        html_body, mimetype = msg.alternatives[0]
        assert mimetype == "text/html"
        assert "New Loan Inquiry" in html_body
        assert "BEJUNDAS FINANCIAL" not in html_body  # uses 'Bejundas Financial Services'
        assert "Bejundas Financial Services" in html_body


@pytest.mark.django_db
class TestInvestmentInquireView:
    def test_get_renders_empty_form(self):
        response = Client().get("/financial/invest/inquire/")
        assert response.status_code == 200
        assert "form" in response.context
        assert response.context.get("offering") is None

    def test_get_with_offering_prefill(self):
        offering = InvestmentOffering.objects.create(
            reference_id="TEST/IO/2026/PREFILL",
            title="Prefilled Round",
            tenure_months=24,
            indicative_rate_pct=Decimal("18.00"),
            min_capital=Decimal("250000.00"),
        )
        response = Client().get(f"/financial/invest/inquire/?offering={offering.slug}")
        assert response.status_code == 200
        assert response.context["offering"] == offering
        assert b"Prefilled Round" in response.content

    def test_post_invalid_redisplays_form(self):
        response = Client().post(
            "/financial/invest/inquire/",
            {"full_name": "", "email": "not-email"},
        )
        assert response.status_code == 200
        assert response.context["form"].errors

    def test_post_valid_creates_row_and_sends_email(self, mailoutbox):
        response = Client().post("/financial/invest/inquire/", _investment_payload())
        assert response.status_code == 200
        assert response.context.get("sent") is True

        inquiry = InvestmentInquiry.objects.get(email="fatma@example.com")
        assert inquiry.full_name == "Fatma Investor"
        assert inquiry.capital_band == "1m_5m"
        assert inquiry.preferred_tenure == "2yr"
        assert inquiry.offering is None
        assert inquiry.status == "new"

        assert len(mailoutbox) == 1
        msg = mailoutbox[0]
        assert "Investment Inquiry" in msg.subject
        assert "Fatma Investor" in msg.body
        assert len(msg.alternatives) == 1
        html_body, _ = msg.alternatives[0]
        assert "New Investment Inquiry" in html_body

    def test_post_valid_attaches_offering_when_query_param_present(self, mailoutbox):
        offering = InvestmentOffering.objects.create(
            reference_id="TEST/IO/2026/ATTACH",
            title="Attached Round",
            tenure_months=12,
            indicative_rate_pct=Decimal("16.50"),
            min_capital=Decimal("250000.00"),
        )
        response = Client().post(
            f"/financial/invest/inquire/?offering={offering.slug}",
            _investment_payload(),
        )
        assert response.status_code == 200
        inquiry = InvestmentInquiry.objects.get(email="fatma@example.com")
        assert inquiry.offering == offering
        # Notification email includes the round reference
        html_body, _ = mailoutbox[0].alternatives[0]
        assert "TEST/IO/2026/ATTACH" in html_body


@pytest.mark.django_db
class TestSitemapIncludesPhase4Pages:
    def test_sitemap_includes_loan_apply_and_invest_inquire(self):
        response = Client().get("/sitemap.xml")
        body = response.content.decode()
        assert "/financial/loans/apply/" in body
        assert "/financial/invest/inquire/" in body
