"""Phase 2 admin smoke tests — each financial admin changelist loads for a staff user."""

from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from apps.financial.models import (
    Certification,
    FinancialService,
    InvestmentInquiry,
    InvestmentOffering,
    LoanInquiry,
    Testimonial,
)


@pytest.fixture
def admin_client(db):
    User = get_user_model()
    user = User.objects.create_user(
        username="finadmin", password="testpass", is_staff=True, is_superuser=True
    )
    client = Client()
    client.force_login(user)
    return client


@pytest.mark.django_db
class TestFinancialAdmins:
    def test_service_changelist_loads(self, admin_client):
        FinancialService.objects.create(
            name="TestPrefix Microfinance", category="loans", summary="x"
        )
        response = admin_client.get(reverse("admin:financial_financialservice_changelist"))
        assert response.status_code == 200
        assert b"TestPrefix Microfinance" in response.content
        # Category pill rendered
        assert b"Microfinance" in response.content

    def test_offering_changelist_loads(self, admin_client):
        InvestmentOffering.objects.create(
            reference_id="TEST/IO/2026/01",
            title="TestPrefix Offering",
            tenure_months=12,
            indicative_rate_pct=Decimal("16.50"),
            min_capital=Decimal("250000.00"),
        )
        response = admin_client.get(reverse("admin:financial_investmentoffering_changelist"))
        assert response.status_code == 200
        assert b"TEST/IO/2026/01" in response.content
        # Rate label and capital formatter rendered
        assert b"16.50%" in response.content
        assert b"TZS 250,000" in response.content

    def test_testimonial_changelist_loads(self, admin_client):
        Testimonial.objects.create(author_name="TestPrefix Author", quote="x")
        response = admin_client.get(reverse("admin:financial_testimonial_changelist"))
        assert response.status_code == 200
        assert b"TestPrefix Author" in response.content

    def test_certification_changelist_loads(self, admin_client):
        Certification.objects.create(name="TestPrefix BoT Reg", issuer="BoT")
        response = admin_client.get(reverse("admin:financial_certification_changelist"))
        assert response.status_code == 200
        assert b"TestPrefix BoT Reg" in response.content

    def test_loan_inquiry_changelist_loads(self, admin_client):
        LoanInquiry.objects.create(
            full_name="TestPrefix Borrower",
            email="x@example.com",
            phone="+255700000000",
            loan_purpose="sme",
            amount_requested=Decimal("5000000.00"),
            tenure_band="12_24",
        )
        response = admin_client.get(reverse("admin:financial_loaninquiry_changelist"))
        assert response.status_code == 200
        assert b"TestPrefix Borrower" in response.content
        assert b"TZS 5,000,000" in response.content
        assert b"New" in response.content  # status pill text

    def test_investment_inquiry_changelist_loads(self, admin_client):
        InvestmentInquiry.objects.create(
            full_name="TestPrefix Investor",
            email="x@example.com",
            phone="+255700000000",
            capital_band="1m_5m",
            preferred_tenure="2yr",
        )
        response = admin_client.get(reverse("admin:financial_investmentinquiry_changelist"))
        assert response.status_code == 200
        assert b"TestPrefix Investor" in response.content
        assert b"New" in response.content

    def test_loan_bulk_action_mark_reviewed(self, admin_client):
        loan = LoanInquiry.objects.create(
            full_name="Bulk Test",
            email="b@example.com",
            phone="+255700000000",
            loan_purpose="personal",
            amount_requested=Decimal("500000.00"),
            tenure_band="6_12",
        )
        url = reverse("admin:financial_loaninquiry_changelist")
        response = admin_client.post(
            url,
            {
                "action": "mark_as_reviewed",
                "_selected_action": [str(loan.pk)],
            },
            follow=True,
        )
        assert response.status_code == 200
        loan.refresh_from_db()
        assert loan.status == "reviewed"

    def test_investment_bulk_action_mark_contacted(self, admin_client):
        inv = InvestmentInquiry.objects.create(
            full_name="Bulk Investor",
            email="b@example.com",
            phone="+255700000000",
            capital_band="250k_1m",
        )
        url = reverse("admin:financial_investmentinquiry_changelist")
        response = admin_client.post(
            url,
            {
                "action": "mark_as_contacted",
                "_selected_action": [str(inv.pk)],
            },
            follow=True,
        )
        assert response.status_code == 200
        inv.refresh_from_db()
        assert inv.status == "contacted"
