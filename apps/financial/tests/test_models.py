"""Phase 2 model tests — use 'TestPrefix' names to avoid collisions
with the Phase 5 seed migration."""

from decimal import Decimal

import pytest

from apps.financial.models import (
    Certification,
    FinancialService,
    InvestmentInquiry,
    InvestmentOffering,
    LoanInquiry,
    Testimonial,
)


@pytest.mark.django_db
class TestFinancialService:
    def test_str(self):
        svc = FinancialService.objects.create(
            name="TestPrefix Microfinance",
            category="loans",
            summary="x",
        )
        assert str(svc) == "TestPrefix Microfinance"

    def test_slug_auto_filled(self):
        svc = FinancialService.objects.create(
            name="TestPrefix Agency Banking",
            category="agency",
            summary="x",
        )
        assert svc.slug == "testprefix-agency-banking"

    def test_default_is_active(self):
        svc = FinancialService.objects.create(
            name="TestPrefix Treasury",
            category="securities",
            summary="x",
        )
        assert svc.is_active is True

    def test_category_display(self):
        svc = FinancialService.objects.create(
            name="TestPrefix Loans",
            category="loans",
            summary="x",
        )
        assert svc.get_category_display() == "Microfinance & Lending"

    def test_default_ordering_scoped_to_test_rows(self):
        a = FinancialService.objects.create(
            name="TestPrefix Alpha", category="loans", summary="x", order=99
        )
        b = FinancialService.objects.create(
            name="TestPrefix Beta", category="loans", summary="x", order=98
        )
        ours = FinancialService.objects.filter(name__startswith="TestPrefix").order_by(
            "order", "name"
        )
        assert list(ours) == [b, a]


@pytest.mark.django_db
class TestInvestmentOffering:
    def test_str_includes_reference_id(self):
        o = InvestmentOffering.objects.create(
            reference_id="TEST/IO/2026/99",
            title="TestPrefix Round",
            tenure_months=12,
            indicative_rate_pct=Decimal("16.50"),
            min_capital=Decimal("250000.00"),
        )
        assert str(o) == "TEST/IO/2026/99 — TestPrefix Round"

    def test_slug_auto_filled_from_reference_id(self):
        o = InvestmentOffering.objects.create(
            reference_id="TEST/IO/2026/77",
            title="TestPrefix Slug",
            tenure_months=24,
            indicative_rate_pct=Decimal("18.00"),
            min_capital=Decimal("250000.00"),
        )
        assert o.slug == "test-io-2026-77"

    def test_default_status_is_upcoming(self):
        o = InvestmentOffering.objects.create(
            reference_id="TEST/IO/2026/88",
            title="TestPrefix Status",
            tenure_months=12,
            indicative_rate_pct=Decimal("16.50"),
            min_capital=Decimal("250000.00"),
        )
        assert o.status == "upcoming"

    def test_default_cadence_is_quarterly(self):
        o = InvestmentOffering.objects.create(
            reference_id="TEST/IO/2026/55",
            title="TestPrefix Cadence",
            tenure_months=12,
            indicative_rate_pct=Decimal("16.50"),
            min_capital=Decimal("250000.00"),
        )
        assert o.payout_cadence == "quarterly"
        assert o.get_payout_cadence_display() == "Quarterly (every 3 months)"

    def test_get_absolute_url_powers_admin_view_on_site(self):
        """get_absolute_url() must point at the public detail page so
        the admin renders the View-on-site button for editors."""
        o = InvestmentOffering.objects.create(
            reference_id="TEST/IO/2026/URL",
            title="TestPrefix URL",
            tenure_months=12,
            indicative_rate_pct=Decimal("16.50"),
            min_capital=Decimal("250000.00"),
        )
        assert o.get_absolute_url() == f"/financial/investments/{o.slug}/"
        # Slug actually slugifies the slashes in the reference id
        assert o.get_absolute_url() == "/financial/investments/test-io-2026-url/"


@pytest.mark.django_db
class TestTestimonial:
    def test_str_with_organisation(self):
        t = Testimonial.objects.create(
            author_name="TestPrefix Author",
            organisation="TestPrefix Org",
            quote="Outstanding partner.",
        )
        assert str(t) == "TestPrefix Author — TestPrefix Org"

    def test_str_without_organisation(self):
        t = Testimonial.objects.create(author_name="TestPrefix Solo", quote="y")
        assert str(t) == "TestPrefix Solo"

    def test_default_not_featured(self):
        t = Testimonial.objects.create(author_name="TestPrefix Anon", quote="y")
        assert t.is_featured is False


@pytest.mark.django_db
class TestCertification:
    def test_str(self):
        c = Certification.objects.create(
            name="TestPrefix BoT Reg",
            issuer="Bank of Tanzania",
        )
        assert str(c) == "TestPrefix BoT Reg (Bank of Tanzania)"

    def test_default_is_active(self):
        c = Certification.objects.create(name="TestPrefix Cert", issuer="x")
        assert c.is_active is True


@pytest.mark.django_db
class TestLoanInquiry:
    def test_str_with_business_name(self):
        loan = LoanInquiry.objects.create(
            full_name="Amina Hassan",
            business_name="Amina Trading",
            email="a@example.com",
            phone="+255700000000",
            loan_purpose="sme",
            amount_requested=Decimal("5000000.00"),
            tenure_band="12_24",
        )
        assert str(loan) == "Amina Trading — SME / Business (New)"

    def test_str_falls_back_to_full_name(self):
        loan = LoanInquiry.objects.create(
            full_name="Juma Personal",
            email="j@example.com",
            phone="+255700000000",
            loan_purpose="personal",
            amount_requested=Decimal("500000.00"),
            tenure_band="6_12",
        )
        assert str(loan) == "Juma Personal — Personal (New)"

    def test_default_status_is_new(self):
        loan = LoanInquiry.objects.create(
            full_name="x",
            email="x@example.com",
            phone="x",
            loan_purpose="group",
            amount_requested=Decimal("1000000.00"),
            tenure_band="under_6",
        )
        assert loan.status == "new"

    def test_default_preferred_contact_is_phone(self):
        loan = LoanInquiry.objects.create(
            full_name="x",
            email="x@example.com",
            phone="x",
            loan_purpose="asset",
            amount_requested=Decimal("1000000.00"),
            tenure_band="over_24",
        )
        assert loan.preferred_contact == "phone"


@pytest.mark.django_db
class TestInvestmentInquiry:
    def test_str_includes_tenure_and_status(self):
        inv = InvestmentInquiry.objects.create(
            full_name="Fatma Investor",
            email="f@example.com",
            phone="+255700000000",
            capital_band="1m_5m",
            preferred_tenure="2yr",
        )
        assert str(inv) == "Fatma Investor — 2 Years (BFS/IO/2026/02) (New)"

    def test_default_status_is_new(self):
        inv = InvestmentInquiry.objects.create(
            full_name="x",
            email="x@example.com",
            phone="x",
            capital_band="250k_1m",
        )
        assert inv.status == "new"

    def test_default_tenure_is_undecided(self):
        inv = InvestmentInquiry.objects.create(
            full_name="x",
            email="x@example.com",
            phone="x",
            capital_band="250k_1m",
        )
        assert inv.preferred_tenure == "undecided"
        assert inv.get_preferred_tenure_display() == "Undecided / Discuss"

    def test_offering_fk_can_be_null(self):
        inv = InvestmentInquiry.objects.create(
            full_name="x",
            email="x@example.com",
            phone="x",
            capital_band="over_10m",
        )
        assert inv.offering is None

    def test_offering_fk_set_null_on_offering_delete(self):
        offering = InvestmentOffering.objects.create(
            reference_id="TEST/IO/DELETE",
            title="To Be Deleted",
            tenure_months=12,
            indicative_rate_pct=Decimal("16.50"),
            min_capital=Decimal("250000.00"),
        )
        inv = InvestmentInquiry.objects.create(
            full_name="x",
            email="x@example.com",
            phone="x",
            capital_band="250k_1m",
            offering=offering,
        )
        offering.delete()
        inv.refresh_from_db()
        assert inv.offering is None
