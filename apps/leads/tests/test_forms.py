import pytest

from apps.leads.forms import LeadForm


@pytest.mark.django_db
class TestLeadForm:
    def test_valid_with_name_and_email(self):
        form = LeadForm({"name": "Test User", "email": "test@example.com"})
        assert form.is_valid()

    def test_valid_with_all_fields(self):
        form = LeadForm(
            {
                "name": "Test User",
                "email": "test@example.com",
                "phone": "+255700000000",
                "message": "I am interested.",
            }
        )
        assert form.is_valid()

    def test_invalid_missing_name(self):
        form = LeadForm({"name": "", "email": "test@example.com"})
        assert not form.is_valid()
        assert "name" in form.errors

    def test_invalid_missing_email(self):
        form = LeadForm({"name": "Test User", "email": ""})
        assert not form.is_valid()
        assert "email" in form.errors

    def test_invalid_bad_email(self):
        form = LeadForm({"name": "Test User", "email": "not-an-email"})
        assert not form.is_valid()
        assert "email" in form.errors

    def test_phone_is_optional(self):
        form = LeadForm({"name": "Test User", "email": "test@example.com", "phone": ""})
        assert form.is_valid()

    def test_message_is_optional(self):
        form = LeadForm({"name": "Test User", "email": "test@example.com", "message": ""})
        assert form.is_valid()
