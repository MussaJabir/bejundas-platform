"""Add the 'insurance' service category and seed 15 insurance products.

Combines two operations into one migration:
  1. AlterField — extend FinancialService.category choices with 'insurance'
  2. RunPython — idempotently upsert 15 insurance product rows

Product list and tagline ("All products can be tailored to individual client
needs") come from the May 2026 client poster. Each product gets a Material
Symbols icon name appropriate to its category — same convention as the
0002 seed, so they render with the same .f-card-icon treatment.
"""

from django.db import migrations, models


INSURANCE_PRODUCTS = [
    {
        "name": "Assets All Risk Insurance",
        "slug": "assets-all-risk-insurance",
        "summary": "Comprehensive cover for business assets including energy installations.",
        "description": (
            "All-risk protection for commercial assets including plant, equipment, "
            "stock, and energy installations. Cover can be tailored to the asset "
            "register of the individual business."
        ),
        "icon": "inventory_2",
        "order": 20,
    },
    {
        "name": "Fire (Consequential Loss) Insurance",
        "slug": "fire-consequential-loss-insurance",
        "summary": "Property fire cover with optional business-interruption extension.",
        "description": (
            "Standard fire and allied perils with a consequential-loss extension "
            "for lost gross profit during the interruption period — covering "
            "fixed costs and standing wages while operations recover."
        ),
        "icon": "local_fire_department",
        "order": 21,
    },
    {
        "name": "Machinery Breakdown (Consequential Loss)",
        "slug": "machinery-breakdown-consequential-loss",
        "summary": "Sudden mechanical / electrical breakdown plus lost-revenue cover.",
        "description": (
            "Cover for unforeseen mechanical, electrical, and electronic "
            "breakdown of plant and machinery, plus consequential loss of "
            "income while replacement parts or repairs are arranged."
        ),
        "icon": "precision_manufacturing",
        "order": 22,
    },
    {
        "name": "Medical Expenses Insurance",
        "slug": "medical-expenses-insurance",
        "summary": "Inpatient and outpatient medical cover for individuals and groups.",
        "description": (
            "Medical schemes covering inpatient, outpatient, maternity, dental, "
            "and optical benefits. Available as individual cover or as a group "
            "scheme for employers."
        ),
        "icon": "medical_services",
        "order": 23,
    },
    {
        "name": "Electronic Equipment Insurance",
        "slug": "electronic-equipment-insurance",
        "summary": "All-risk cover for computers, servers, and electronic equipment.",
        "description": (
            "All-risk protection for electronic equipment — computers, servers, "
            "telecoms, POS terminals, and audio-visual systems. Covers physical "
            "loss / damage plus consequential data reinstatement costs."
        ),
        "icon": "devices",
        "order": 24,
    },
    {
        "name": "Burglary Insurance",
        "slug": "burglary-insurance",
        "summary": "Cover for theft following forcible entry into business premises.",
        "description": (
            "Cover for loss of stock, equipment, and money following forcible "
            "and violent entry into business premises. Sums insured and "
            "deductibles negotiated against the client's risk profile."
        ),
        "icon": "lock",
        "order": 25,
    },
    {
        "name": "Motor Vehicle Insurance & Goods in Transit",
        "slug": "motor-vehicle-insurance-and-goods-in-transit",
        "summary": "Comprehensive motor cover plus cover for goods carried.",
        "description": (
            "Comprehensive, third-party fire & theft, and third-party only "
            "motor cover for private and commercial fleets, plus goods-in-transit "
            "cover for cargo carried by road across Tanzania and the EAC corridor."
        ),
        "icon": "local_shipping",
        "order": 26,
    },
    {
        "name": "Fidelity Guarantee",
        "slug": "fidelity-guarantee",
        "summary": "Protection against employee dishonesty and embezzlement.",
        "description": (
            "Indemnity against direct financial loss caused by dishonest acts "
            "of employees handling cash, stock, or accounts. Cover written on "
            "named-individual or blanket basis."
        ),
        "icon": "verified_user",
        "order": 27,
    },
    {
        "name": "General Public Liability",
        "slug": "general-public-liability",
        "summary": "Third-party injury and property damage cover for businesses.",
        "description": (
            "Indemnity against legal liability to third parties for accidental "
            "bodily injury or property damage arising out of the business — "
            "covering legal costs and awarded damages up to the policy limit."
        ),
        "icon": "support",
        "order": 28,
    },
    {
        "name": "Workmen's Compensation & Employer's Liability",
        "slug": "workmens-compensation-and-employers-liability",
        "summary": "Statutory employee injury benefits plus common-law employer cover.",
        "description": (
            "Workmen's Compensation Act benefits for employees injured in the "
            "course of employment, combined with Employer's Liability cover "
            "for common-law claims that exceed the statutory schedule."
        ),
        "icon": "engineering",
        "order": 29,
    },
    {
        "name": "Group Personal Accident Insurance",
        "slug": "group-personal-accident-insurance",
        "summary": "24-hour worldwide accident cover for groups of employees.",
        "description": (
            "Lump-sum benefits for accidental death, permanent disability, "
            "temporary total disablement, and medical reimbursement — 24 hours "
            "worldwide, written on a group / scheme basis."
        ),
        "icon": "personal_injury",
        "order": 30,
    },
    {
        "name": "Money Insurance",
        "slug": "money-insurance",
        "summary": "Cover for cash in transit, on premises, and in safes.",
        "description": (
            "Protects cash and negotiable instruments while in transit (e.g. "
            "to and from the bank), held on the business premises during "
            "working hours, and locked in safes overnight."
        ),
        "icon": "payments",
        "order": 31,
    },
    {
        "name": "Group Life Insurance",
        "slug": "group-life-insurance",
        "summary": "Death-in-service cover for employees on a group scheme.",
        "description": (
            "Lump-sum benefit payable to a nominated beneficiary on the death "
            "of an employee, while the employee is a member of the scheme. "
            "Common as part of an employee benefits package."
        ),
        "icon": "family_restroom",
        "order": 32,
    },
    {
        "name": "Group Funeral Expenses Insurance",
        "slug": "group-funeral-expenses-insurance",
        "summary": "Funeral cost benefits for the employee and immediate family.",
        "description": (
            "Lump-sum funeral benefit covering the employee, spouse, and "
            "dependants. Designed to provide quick cash to settle funeral "
            "expenses without waiting on a full death-claim process."
        ),
        "icon": "volunteer_activism",
        "order": 33,
    },
    {
        "name": "Bonds of All Kinds",
        "slug": "bonds-of-all-kinds",
        "summary": "Bid, performance, advance-payment, and customs bonds.",
        "description": (
            "Surety bonds issued in favour of project owners, government "
            "agencies, and customs authorities — including bid bonds, "
            "performance bonds, advance-payment guarantees, and customs / "
            "warehousing bonds."
        ),
        "icon": "gavel",
        "order": 34,
    },
]


def seed_forward(apps, schema_editor):
    FinancialService = apps.get_model("financial", "FinancialService")
    for entry in INSURANCE_PRODUCTS:
        slug = entry["slug"]
        defaults = {k: v for k, v in entry.items() if k != "slug"}
        defaults["category"] = "insurance"
        FinancialService.objects.update_or_create(slug=slug, defaults=defaults)


def seed_reverse(apps, schema_editor):
    FinancialService = apps.get_model("financial", "FinancialService")
    FinancialService.objects.filter(
        slug__in=[p["slug"] for p in INSURANCE_PRODUCTS]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("financial", "0002_seed_curated_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="financialservice",
            name="category",
            field=models.CharField(
                choices=[
                    ("loans", "Microfinance & Lending"),
                    ("investments", "Investments & Partnerships"),
                    ("agency", "Agency & Franchising"),
                    ("securities", "Government Securities & DSE"),
                    ("auto", "Auto & Asset Services"),
                    ("insurance", "Insurance Products"),
                ],
                help_text="Groups services on the /financial/services/ page.",
                max_length=20,
            ),
        ),
        migrations.RunPython(seed_forward, seed_reverse),
    ]
