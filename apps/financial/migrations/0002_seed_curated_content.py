"""Seed Tanzania-flavoured curated content for the financial vertical.

Idempotent — uses update_or_create so re-running the migration won't
duplicate rows. All entries are placeholder content that admin users
can edit row-by-row when real client content arrives.

Investment offerings are seeded from the BFS/IO/2026/01 and /02 rounds
advertised on the May 2026 WhatsApp posters. Dates use the Phase 2
intake calendar (capital deadline 30 June 2026, 1-year settlement
30 June 2027, 2-year settlement 30 June 2028).
"""

from datetime import date
from decimal import Decimal

from django.db import migrations


SERVICES = [
    # ── Loans ──────────────────────────────────────────────────────
    {
        "name": "Personal Loans",
        "slug": "personal-loans",
        "category": "loans",
        "summary": "Short-term microfinance for individuals — favourable rates and negotiable schedules.",
        "description": (
            "Personal loans for salaried, self-employed, and informal-sector clients "
            "across Dar es Salaam and beyond. Tenures from a few weeks to two years. "
            "Repayment schedules negotiated case-by-case to fit your income cycle."
        ),
        "icon": "person",
        "order": 1,
    },
    {
        "name": "SME & Corporate Loans",
        "slug": "sme-corporate-loans",
        "category": "loans",
        "summary": "Working capital and growth finance for Tanzanian small and medium businesses.",
        "description": (
            "Inventory finance, equipment purchase, working capital lines, and growth "
            "loans for established Tanzanian SMEs. We look at the business cashflow and "
            "track record — not only collateral — when assessing applications."
        ),
        "icon": "business",
        "order": 2,
    },
    {
        "name": "Group Loans",
        "slug": "group-loans",
        "category": "loans",
        "summary": "Solidarity group lending for cooperatives, women's groups, and savings circles.",
        "description": (
            "Group lending built on the trust model — solidarity guarantees, joint "
            "liability, and weekly or monthly repayment cycles. We work with VICOBA, "
            "SACCOS, and informal savings groups across the country."
        ),
        "icon": "groups",
        "order": 3,
    },
    {
        "name": "Asset Refinancing",
        "slug": "asset-refinancing",
        "category": "loans",
        "summary": "Refinancing against retail businesses, vehicles, and productive assets.",
        "description": (
            "Unlock capital tied up in productive assets. We refinance against retail "
            "businesses, commercial vehicles, machinery, and other working assets — "
            "with the asset itself as security and your cashflow guiding the schedule."
        ),
        "icon": "redo",
        "order": 4,
    },
    # ── Agency ─────────────────────────────────────────────────────
    {
        "name": "Mobile Network & Banking Agency",
        "slug": "agency-banking",
        "category": "agency",
        "summary": "Cash-in, cash-out, deposits and bill payments across mobile money and banking partners.",
        "description": (
            "Agency banking and mobile money services — deposits, withdrawals, "
            "transfers, bill payments, and salary disbursements. We operate as agents "
            "for leading commercial banks and mobile network operators."
        ),
        "icon": "account_balance",
        "order": 5,
    },
    {
        "name": "Banking Franchise Partnership",
        "slug": "banking-franchise",
        "category": "agency",
        "summary": "Set up a banking branch franchise under our partnership network.",
        "description": (
            "We partner with banking institutions to franchise neighbourhood branches "
            "under their network. If you have the location and the local credibility, "
            "we provide the operating capital, training, and back-office integration."
        ),
        "icon": "storefront",
        "order": 6,
    },
    # ── Securities ─────────────────────────────────────────────────
    {
        "name": "Treasury Bills & Bonds",
        "slug": "treasury-bills-bonds",
        "category": "securities",
        "summary": "Access government Treasury Bills (91-, 182-, 364-day) and long-dated bonds.",
        "description": (
            "We help clients participate in Tanzanian government securities — Treasury "
            "Bills for short-term placement and long-dated bonds for capital "
            "preservation. Suitable for clients with available capital looking for "
            "low-risk fixed-income exposure."
        ),
        "icon": "receipt_long",
        "order": 7,
    },
    {
        "name": "DSE Stock Market & Mutual Funds",
        "slug": "dse-stock-mutual-funds",
        "category": "securities",
        "summary": "Dar es Salaam Stock Exchange listings and mutual fund placements (ETFs & Faida Fund).",
        "description": (
            "Equity participation on the Dar es Salaam Stock Exchange (DSE) plus "
            "placements in mutual funds and ETFs including the Faida Fund. We advise "
            "on allocation, time horizon, and the practical mechanics of opening a "
            "Central Depository System (CDS) account."
        ),
        "icon": "trending_up",
        "order": 8,
    },
    # ── Auto ───────────────────────────────────────────────────────
    {
        "name": "Auto Services",
        "slug": "auto-services",
        "category": "auto",
        "summary": "Vehicle-backed finance and asset acquisition for commercial fleets.",
        "description": (
            "Vehicle financing for commercial operators — bodaboda, daladala, taxi "
            "fleets, and SME delivery vans. We structure repayments around vehicle "
            "earning days and offer fleet-scale agreements for established operators."
        ),
        "icon": "directions_car",
        "order": 9,
    },
]


OFFERINGS = [
    {
        "reference_id": "BFS/IO/2026/01",
        "slug": "bfs-io-2026-01",
        "title": "1-Year Investment Partnership",
        "tenure_months": 12,
        "indicative_rate_pct": Decimal("16.50"),
        "min_capital": Decimal("250000.00"),
        "payout_cadence": "quarterly",
        "opens_at": date(2026, 5, 11),
        "closes_at": date(2026, 6, 30),
        "settlement_date": date(2027, 6, 30),
        "status": "open",
        "description": (
            "A 12-month private placement partnership with quarterly interest "
            "payouts. Capital is deployed across the company's mixed business "
            "ventures — microfinance lending, agency banking operations, "
            "government securities, and retail refinancing. Returns are "
            "indicative; actual performance depends on the underlying portfolio."
        ),
        "payout_calendar_notes": (
            "Phase 2 capital deadline: 30 June 2026.\n"
            "\n"
            "Interest payment dates:\n"
            "  • 1st quarter — 30 September 2026\n"
            "  • 2nd quarter — 31 December 2026\n"
            "  • 3rd quarter — 31 March 2027\n"
            "  • 4th quarter — 30 June 2027\n"
            "\n"
            "Principal returned: 30 June 2027.\n"
            "Day-count convention: 365 days."
        ),
        "is_featured": True,
        "order": 1,
    },
    {
        "reference_id": "BFS/IO/2026/02",
        "slug": "bfs-io-2026-02",
        "title": "2-Year Investment Partnership",
        "tenure_months": 24,
        "indicative_rate_pct": Decimal("18.00"),
        "min_capital": Decimal("250000.00"),
        "payout_cadence": "quarterly",
        "opens_at": date(2026, 5, 11),
        "closes_at": date(2026, 6, 30),
        "settlement_date": date(2028, 6, 30),
        "status": "open",
        "description": (
            "A 24-month private placement partnership with quarterly interest "
            "payouts at a higher indicative rate than the 1-year round. Same "
            "deployment basket as the 1-year round — microfinance, agency "
            "banking, securities, and retail refinancing. Suitable for clients "
            "comfortable with a two-year horizon."
        ),
        "payout_calendar_notes": (
            "Phase 2 capital deadline: 30 June 2026.\n"
            "\n"
            "Interest payment dates (8 quarterly payouts):\n"
            "  • 30 September 2026\n"
            "  • 31 December 2026\n"
            "  • 31 March 2027\n"
            "  • 30 June 2027\n"
            "  • 30 September 2027\n"
            "  • 31 December 2027\n"
            "  • 31 March 2028\n"
            "  • 30 June 2028\n"
            "\n"
            "Principal returned: 30 June 2028.\n"
            "Day-count convention: 730 days."
        ),
        "is_featured": True,
        "order": 2,
    },
]


TESTIMONIALS = [
    {
        "author_name": "Halima Mwakipesile",
        "author_role": "Owner",
        "organisation": "Halima Trading Stores, Mwanza",
        "quote": (
            "Bejundas Financial gave us a working-capital loan when the bank "
            "was still asking for collateral we did not have. The terms were "
            "fair, the repayment schedule fit our cash cycle, and the team "
            "took the time to understand the business."
        ),
        "is_featured": True,
        "order": 1,
    },
    {
        "author_name": "Joseph Mwakatobe",
        "author_role": "Private Investor",
        "organisation": "Dar es Salaam",
        "quote": (
            "I have been investing with Bejundas for over a year. The quarterly "
            "payouts arrive on time, the team is transparent about how the "
            "capital is deployed, and the indicative rates are competitive "
            "compared to what the banks offer."
        ),
        "is_featured": True,
        "order": 2,
    },
    {
        "author_name": "Neema Kapinga",
        "author_role": "Chairlady",
        "organisation": "Tumaini Women's Cooperative",
        "quote": (
            "We started with a small group loan three years ago. Today our "
            "cooperative has 42 members and we have graduated to larger "
            "facilities. Bejundas grew with us — that matters in this market."
        ),
        "is_featured": True,
        "order": 3,
    },
    {
        "author_name": "Emmanuel Rwambali",
        "author_role": "Director",
        "organisation": "Rwambali Logistics Ltd",
        "quote": (
            "We needed to refinance against our fleet to acquire two new "
            "trucks for a contract. Bejundas structured the deal in under two "
            "weeks. The terms were realistic and the schedule worked with our "
            "monthly contract billings."
        ),
        "is_featured": False,
        "order": 4,
    },
]


def seed_forward(apps, schema_editor):
    FinancialService = apps.get_model("financial", "FinancialService")
    InvestmentOffering = apps.get_model("financial", "InvestmentOffering")
    Testimonial = apps.get_model("financial", "Testimonial")

    for entry in SERVICES:
        slug = entry["slug"]
        defaults = {k: v for k, v in entry.items() if k != "slug"}
        FinancialService.objects.update_or_create(slug=slug, defaults=defaults)

    for entry in OFFERINGS:
        ref = entry["reference_id"]
        defaults = {k: v for k, v in entry.items() if k != "reference_id"}
        InvestmentOffering.objects.update_or_create(reference_id=ref, defaults=defaults)

    for entry in TESTIMONIALS:
        author = entry["author_name"]
        organisation = entry.get("organisation", "")
        defaults = {k: v for k, v in entry.items() if k not in ("author_name", "organisation")}
        defaults["organisation"] = organisation
        Testimonial.objects.update_or_create(
            author_name=author,
            organisation=organisation,
            defaults=defaults,
        )


def seed_reverse(apps, schema_editor):
    """Remove only the rows seeded by this migration — admin-added rows survive."""
    FinancialService = apps.get_model("financial", "FinancialService")
    InvestmentOffering = apps.get_model("financial", "InvestmentOffering")
    Testimonial = apps.get_model("financial", "Testimonial")

    FinancialService.objects.filter(slug__in=[s["slug"] for s in SERVICES]).delete()
    InvestmentOffering.objects.filter(
        reference_id__in=[o["reference_id"] for o in OFFERINGS]
    ).delete()
    Testimonial.objects.filter(
        author_name__in=[t["author_name"] for t in TESTIMONIALS]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("financial", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_forward, seed_reverse),
    ]
