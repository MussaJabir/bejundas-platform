"""Phase 5 — verify the seed migration 0002_seed_curated_content
populates the catalogue with the right shape and the right numbers."""

from decimal import Decimal

import pytest

from apps.financial.models import FinancialService, InvestmentOffering, Testimonial


@pytest.mark.django_db
class TestSeededContent:
    def test_9_services_seeded(self):
        assert FinancialService.objects.count() == 9

    def test_services_cover_four_categories(self):
        categories = set(FinancialService.objects.values_list("category", flat=True))
        # Phase 5 seed covers loans / agency / securities / auto (no 'investments'
        # service rows — that category points users at /financial/investments/).
        assert categories == {"loans", "agency", "securities", "auto"}

    def test_2_offerings_seeded(self):
        assert InvestmentOffering.objects.count() == 2

    def test_offering_one_year_round_matches_poster(self):
        o = InvestmentOffering.objects.get(reference_id="BFS/IO/2026/01")
        assert o.tenure_months == 12
        assert o.indicative_rate_pct == Decimal("16.50")
        assert o.min_capital == Decimal("250000.00")
        assert o.payout_cadence == "quarterly"
        assert o.status == "open"
        assert o.is_featured is True

    def test_offering_two_year_round_matches_poster(self):
        o = InvestmentOffering.objects.get(reference_id="BFS/IO/2026/02")
        assert o.tenure_months == 24
        assert o.indicative_rate_pct == Decimal("18.00")
        assert o.min_capital == Decimal("250000.00")
        assert o.payout_cadence == "quarterly"
        assert o.status == "open"
        assert o.is_featured is True

    def test_offering_slugs_are_url_safe(self):
        # "BFS/IO/2026/01" slugified must work in a path-based URL.
        assert InvestmentOffering.objects.filter(slug="bfs-io-2026-01").exists()
        assert InvestmentOffering.objects.filter(slug="bfs-io-2026-02").exists()

    def test_4_testimonials_seeded(self):
        assert Testimonial.objects.count() == 4

    def test_three_testimonials_featured(self):
        assert Testimonial.objects.filter(is_featured=True).count() == 3

    def test_seeded_offering_detail_url_renders(self, client):
        response = client.get("/financial/investments/bfs-io-2026-01/")
        assert response.status_code == 200
        assert b"BFS/IO/2026/01" in response.content
        assert b"1-Year Investment Partnership" in response.content
        assert b"16.50" in response.content
