"""Construction email-send failures must NOT 500 the visitor."""

from unittest.mock import patch

import pytest
from django.test import Client

from apps.construction.models import QuoteRequest


@pytest.mark.django_db
class TestConstructionContactEmailResilience:
    def test_smtp_failure_does_not_500(self):
        with patch(
            "apps.construction.forms.ContactForm.send_email",
            side_effect=ConnectionError("SMTP down"),
        ):
            response = Client().post(
                "/construction/contact/",
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
class TestConstructionQuoteEmailResilience:
    def _payload(self):
        return {
            "full_name": "Resilience RFP",
            "email": "res-rfp@example.com",
            "phone": "+255712345678",
            "project_type": "commercial",
            "location_region": "Dar es Salaam",
            "location_district": "Ilala",
            "scope_description": (
                "A reasonably detailed scope describing what we want to "
                "build. This needs to exceed the 50 character minimum so "
                "the form passes validation. Plenty of detail here."
            ),
            "budget_range": "50m_200m",
            "timeline": "3_6",
        }

    def test_smtp_failure_still_saves_quote_and_renders_success(self):
        with patch(
            "apps.construction.forms.QuoteRequestForm.send_notification",
            side_effect=ConnectionError("SMTP down"),
        ):
            response = Client().post("/construction/quote/", self._payload())

        # User sees the success page (NOT a 500) ...
        assert response.status_code == 200
        assert response.context.get("sent") is True
        # ... and the quote request is captured in the DB.
        assert QuoteRequest.objects.filter(email="res-rfp@example.com").exists()
