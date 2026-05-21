"""Email-send failures must NOT 500 the visitor — the row is saved,
the inquiry is captured; SMTP is best-effort."""

from unittest.mock import patch

import pytest
from django.test import Client

from apps.financial.models import InvestmentInquiry, LoanInquiry


@pytest.mark.django_db
class TestFinancialContactEmailResilience:
    def test_smtp_failure_does_not_500(self):
        with patch(
            "apps.financial.forms.ContactForm.send_email",
            side_effect=ConnectionError("SMTP down"),
        ):
            response = Client().post(
                "/financial/contact/",
                {
                    "name": "Resilience Test",
                    "email": "test@example.com",
                    "phone": "+255712345678",
                    "subject": "Test",
                    "message": "Hi.",
                },
            )
        assert response.status_code == 200
        assert response.context.get("sent") is True


@pytest.mark.django_db
class TestLoanApplyEmailResilience:
    def _payload(self):
        return {
            "full_name": "Resilient Borrower",
            "email": "res-loan@example.com",
            "phone": "+255712345678",
            "loan_purpose": "sme",
            "amount_requested": "1000000",
            "tenure_band": "6_12",
            "preferred_contact": "phone",
        }

    def test_smtp_failure_still_saves_row_and_renders_success(self):
        with patch(
            "apps.financial.forms.LoanInquiryForm.send_notification",
            side_effect=ConnectionError("SMTP down"),
        ):
            response = Client().post("/financial/loans/apply/", self._payload())

        # User sees the success page (NOT a 500) ...
        assert response.status_code == 200
        assert response.context.get("sent") is True
        # ... and the row is captured in the DB so the team can follow up.
        assert LoanInquiry.objects.filter(email="res-loan@example.com").exists()

    def test_template_rendering_error_does_not_500(self):
        """A bug in the email template should not block the user flow."""
        with patch(
            "apps.financial.forms.LoanInquiryForm.send_notification",
            side_effect=Exception("template syntax error"),
        ):
            response = Client().post("/financial/loans/apply/", self._payload())
        assert response.status_code == 200
        assert response.context.get("sent") is True


@pytest.mark.django_db
class TestInvestmentInquireEmailResilience:
    def _payload(self):
        return {
            "full_name": "Resilient Investor",
            "email": "res-invest@example.com",
            "phone": "+255712345678",
            "capital_band": "1m_5m",
            "preferred_tenure": "2yr",
            "funding_source": "savings",
            "preferred_contact": "whatsapp",
        }

    def test_smtp_failure_still_saves_row_and_renders_success(self):
        with patch(
            "apps.financial.forms.InvestmentInquiryForm.send_notification",
            side_effect=ConnectionError("SMTP down"),
        ):
            response = Client().post("/financial/invest/inquire/", self._payload())

        assert response.status_code == 200
        assert response.context.get("sent") is True
        assert InvestmentInquiry.objects.filter(email="res-invest@example.com").exists()
