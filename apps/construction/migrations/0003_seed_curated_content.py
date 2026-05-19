"""Seed Tanzania-flavoured curated content for the construction vertical.

Idempotent — uses update_or_create so re-running the migration won't
duplicate rows. All entries are placeholder content that admin users
can edit row-by-row when real client content arrives.
"""

from django.db import migrations


SERVICES = [
    {
        "name": "Residential Builds",
        "slug": "residential-builds",
        "summary": "Custom homes, villas and multi-unit residential developments — turnkey or staged.",
        "description": (
            "We deliver single-villa builds through to multi-unit gated communities. "
            "Every residential project is run by a dedicated project manager with "
            "weekly progress reports and on-site quality control. From Masaki "
            "townhouses to lakeside retreats, we work to your specification, "
            "your timeline, and your budget."
        ),
        "icon": "home",
        "order": 1,
    },
    {
        "name": "Commercial Construction",
        "slug": "commercial-construction",
        "summary": "Office buildings, retail, warehouses and hospitality — built for working environments.",
        "description": (
            "Mid-rise office blocks, retail centres, hotel developments, and mixed-use "
            "schemes. We coordinate every trade in-house — structural, MEP, fit-out — "
            "so you have one accountable contractor from foundations to handover."
        ),
        "icon": "domain",
        "order": 2,
    },
    {
        "name": "Civil Works",
        "slug": "civil-works",
        "summary": "Roads, bridges, drainage and site infrastructure — to NCC Class standards.",
        "description": (
            "Heavy civil engineering executed by NCC-registered teams. Asphalt and "
            "concrete pavement, drainage networks, retaining structures, bridge approach "
            "works, and complete site infrastructure for commercial and industrial sites."
        ),
        "icon": "construction",
        "order": 3,
    },
    {
        "name": "MEP Installation",
        "slug": "mep-installation",
        "summary": "Mechanical, electrical and plumbing — coordinated under one project manager.",
        "description": (
            "We install and commission complete MEP packages — HVAC, plumbing, "
            "electrical distribution, fire safety systems, and low-voltage networks. "
            "All work is coordinated within our main contracting flow, eliminating "
            "interface risk with separate sub-contractors."
        ),
        "icon": "bolt",
        "order": 4,
    },
    {
        "name": "Interior Fit-out",
        "slug": "interior-fit-out",
        "summary": "Partitioning, ceilings, finishes and FF&E — handover-ready turnkey delivery.",
        "description": (
            "From boutique retail interiors to corporate office floors — partitioning, "
            "suspended ceilings, joinery, flooring, wall finishes, and FF&E procurement "
            "and installation. We deliver fit-outs that are ready to operate from day one."
        ),
        "icon": "chair",
        "order": 5,
    },
    {
        "name": "Project Management",
        "slug": "project-management",
        "summary": "Scope, schedule, cost control and contractor coordination — on your behalf.",
        "description": (
            "When you've engaged multiple contractors and need an experienced owner's "
            "representative, our project management service takes the load. Schedule "
            "control, cost tracking, change-order management, contractor coordination, "
            "and structured reporting against agreed KPIs."
        ),
        "icon": "task_alt",
        "order": 6,
    },
    {
        "name": "Design-Build",
        "slug": "design-build",
        "summary": "Single accountable team from concept to handover — faster, fewer interfaces.",
        "description": (
            "We bring design and construction under one roof. Architecture, structural "
            "engineering, MEP design, and construction execution by a single team. The "
            "result: faster delivery, fewer change orders, and one point of accountability."
        ),
        "icon": "architecture",
        "order": 7,
    },
    {
        "name": "Renovations & Restoration",
        "slug": "renovations-restoration",
        "summary": "Heritage restorations and full-scope refurbishments — bringing assets back to spec.",
        "description": (
            "Tired office floors, ageing hotel properties, structural restoration for "
            "heritage buildings — we deliver renovation programs that preserve what "
            "works and replace what doesn't. Minimal disruption to operations where the "
            "building stays in use during the works."
        ),
        "icon": "build",
        "order": 8,
    },
]


PROJECTS = [
    {
        "title": "Masaki Residential Tower",
        "slug": "masaki-residential-tower",
        "sector": "residential",
        "location_city": "Dar es Salaam",
        "location_region": "Masaki",
        "year_completed": 2024,
        "description": (
            "A 14-storey residential tower delivering 56 luxury apartments on the "
            "Masaki peninsula. Full design-build engagement covering structural shell, "
            "MEP installation, fit-out, and rooftop amenities including pool and gym. "
            "Delivered on a 22-month programme to within 3% of the agreed budget."
        ),
        "is_featured": True,
        "order": 1,
    },
    {
        "title": "Dodoma Logistics Hub",
        "slug": "dodoma-logistics-hub",
        "sector": "industrial",
        "location_city": "Dodoma",
        "location_region": "Dodoma Region",
        "year_completed": 2023,
        "description": (
            "An 18,000 m² logistics and distribution facility for a regional FMCG client. "
            "Pre-engineered steel frame, racking-grade concrete slab, loading docks for "
            "24 vehicles, and integrated office wing. Designed for 24/7 operations with "
            "redundant power and water infrastructure."
        ),
        "is_featured": True,
        "order": 2,
    },
    {
        "title": "Mwanza Ring Road · Section 4",
        "slug": "mwanza-ring-road-section-4",
        "sector": "civil",
        "location_city": "Mwanza",
        "location_region": "Mwanza Region",
        "year_completed": 2022,
        "description": (
            "12 km of dual-carriageway as part of the Mwanza ring road infrastructure "
            "programme. Earthworks, drainage, asphalt pavement, signage, and street "
            "lighting. Completed ahead of the public-sector schedule following close "
            "coordination with TANROADS and the Mwanza City Council."
        ),
        "is_featured": False,
        "order": 3,
    },
    {
        "title": "Zanzibar Boutique Hotel",
        "slug": "zanzibar-boutique-hotel",
        "sector": "commercial",
        "location_city": "Zanzibar",
        "location_region": "Stone Town",
        "year_completed": 2024,
        "description": (
            "Restoration and extension of a heritage building in Stone Town into a "
            "32-key boutique hotel. Sensitive structural restoration preserving the "
            "original façade and courtyards, with full modern MEP retrofit hidden in "
            "purpose-built service voids. Recognised by the Stone Town Conservation Authority."
        ),
        "is_featured": True,
        "order": 4,
    },
    {
        "title": "Mbeya Secondary School Block",
        "slug": "mbeya-secondary-school-block",
        "sector": "commercial",
        "location_city": "Mbeya",
        "location_region": "Mbeya Region",
        "year_completed": 2023,
        "description": (
            "A new 12-classroom teaching block plus science laboratory wing for a "
            "government secondary school in Mbeya. Single-storey reinforced concrete "
            "frame with corrugated steel roofing, ceramic-tiled corridors, and full "
            "ablution facilities. Delivered during school holidays to minimise disruption."
        ),
        "is_featured": False,
        "order": 5,
    },
    {
        "title": "Arusha Coffee Processing Facility",
        "slug": "arusha-coffee-processing-facility",
        "sector": "industrial",
        "location_city": "Arusha",
        "location_region": "Arusha Region",
        "year_completed": 2022,
        "description": (
            "Coffee processing and packaging facility for a regional cooperative. "
            "Includes washing stations, drying patios, sorting halls, cold storage, and "
            "a packaging line. Specialist food-grade finishes throughout and a sustainable "
            "water recovery system installed at the client's request."
        ),
        "is_featured": False,
        "order": 6,
    },
    {
        "title": "Bagamoyo Tourism Lodge",
        "slug": "bagamoyo-tourism-lodge",
        "sector": "commercial",
        "location_city": "Bagamoyo",
        "location_region": "Pwani Region",
        "year_completed": 2025,
        "description": (
            "A 24-room eco-lodge on the Bagamoyo coast. Locally sourced makuti roofing, "
            "rammed-earth walls, off-grid solar with battery storage, and tertiary "
            "wastewater treatment. The full programme was executed using local labour "
            "and trained 18 community apprentices through to completion."
        ),
        "is_featured": False,
        "order": 7,
    },
    {
        "title": "Iringa District Hospital — New Wing",
        "slug": "iringa-district-hospital-new-wing",
        "sector": "commercial",
        "location_city": "Iringa",
        "location_region": "Iringa Region",
        "year_completed": 2024,
        "description": (
            "A 48-bed in-patient wing extending the existing district hospital. "
            "Includes a 4-theatre surgical suite, ICU bay, medical gas distribution, "
            "and a dedicated emergency entrance. Delivered alongside continued hospital "
            "operations with strict infection-control protocols on every shift."
        ),
        "is_featured": False,
        "order": 8,
    },
    {
        "title": "Kigamboni Bridge Approach Roads",
        "slug": "kigamboni-bridge-approach-roads",
        "sector": "civil",
        "location_city": "Dar es Salaam",
        "location_region": "Kigamboni",
        "year_completed": 2021,
        "description": (
            "Approach roads and tie-ins on the Kigamboni side of the Nyerere Bridge. "
            "4.2 km of dual carriageway with associated drainage, retaining structures, "
            "and pedestrian footbridges. Engineered to handle the projected freight "
            "load shifts from the port expansion programme."
        ),
        "is_featured": False,
        "order": 9,
    },
    {
        "title": "Tanga Port Warehouse Fit-out",
        "slug": "tanga-port-warehouse-fit-out",
        "sector": "fitout",
        "location_city": "Tanga",
        "location_region": "Tanga Region",
        "year_completed": 2024,
        "description": (
            "Fit-out of a 6,200 m² dry-goods warehouse adjacent to Tanga Port. "
            "Heavy-duty racking, integrated WMS-ready conveyors, ESFR sprinkler "
            "upgrade, and a 600 m² climate-controlled section for sensitive cargo. "
            "Handover achieved 11 days ahead of programme."
        ),
        "is_featured": False,
        "order": 10,
    },
]


TESTIMONIALS = [
    {
        "author_name": "Amina Hassan",
        "author_role": "Managing Director",
        "organisation": "Hassan Holdings Ltd",
        "quote": (
            "Bejundas Construction delivered our Masaki tower three weeks ahead of "
            "schedule and well within budget. Their weekly reporting kept us informed "
            "without ever feeling like we were managing the project ourselves. We will "
            "absolutely work with them on our next development."
        ),
        "is_featured": True,
        "order": 1,
    },
    {
        "author_name": "Joseph Mwangi",
        "author_role": "Operations Director",
        "organisation": "Tanzania Logistics Corp",
        "quote": (
            "Our Dodoma hub had a hard deadline tied to a contract start date. Bejundas "
            "ran the programme tightly, escalated risks early, and handed over a facility "
            "we could begin operating from on day one. Professional from start to finish."
        ),
        "is_featured": True,
        "order": 2,
    },
    {
        "author_name": "Grace Mwamba",
        "author_role": "Head Teacher",
        "organisation": "Mbeya Secondary School",
        "quote": (
            "The new classroom block transformed what we could offer our students. "
            "Bejundas worked entirely around our school calendar — the children walked "
            "back from holiday into brand new facilities and never lost a day of teaching."
        ),
        "is_featured": False,
        "order": 3,
    },
    {
        "author_name": "Salim Juma",
        "author_role": "Cooperative Chairman",
        "organisation": "Arusha Highland Coffee Cooperative",
        "quote": (
            "Bejundas took our brief — a processing facility we could be proud of — and "
            "delivered something better than we'd dared imagine. The water recovery system "
            "they suggested has cut our utility costs more than we expected. Excellent partners."
        ),
        "is_featured": True,
        "order": 4,
    },
]


CERTIFICATIONS = [
    {
        "name": "NCC Class 1 Registration",
        "issuer": "National Construction Council of Tanzania",
        "year_awarded": 2018,
        "order": 1,
    },
    {
        "name": "ISO 9001:2015 — Quality Management",
        "issuer": "International Organization for Standardization",
        "year_awarded": 2021,
        "order": 2,
    },
    {
        "name": "ISO 14001:2015 — Environmental Management",
        "issuer": "International Organization for Standardization",
        "year_awarded": 2022,
        "order": 3,
    },
    {
        "name": "OSHA Workplace Safety Compliance",
        "issuer": "Occupational Safety and Health Authority",
        "year_awarded": 2023,
        "order": 4,
    },
]


def seed_content(apps, schema_editor):
    ConstructionService = apps.get_model("construction", "ConstructionService")
    Project = apps.get_model("construction", "Project")
    Testimonial = apps.get_model("construction", "Testimonial")
    Certification = apps.get_model("construction", "Certification")

    for svc in SERVICES:
        ConstructionService.objects.update_or_create(
            slug=svc["slug"],
            defaults={k: v for k, v in svc.items() if k != "slug"},
        )

    for proj in PROJECTS:
        Project.objects.update_or_create(
            slug=proj["slug"],
            defaults={k: v for k, v in proj.items() if k != "slug"},
        )

    for t in TESTIMONIALS:
        Testimonial.objects.update_or_create(
            author_name=t["author_name"],
            organisation=t["organisation"],
            defaults={k: v for k, v in t.items() if k not in ("author_name", "organisation")},
        )

    for cert in CERTIFICATIONS:
        Certification.objects.update_or_create(
            name=cert["name"],
            defaults={k: v for k, v in cert.items() if k != "name"},
        )


def unseed_content(apps, schema_editor):
    """Remove the seeded rows on migration reverse."""
    ConstructionService = apps.get_model("construction", "ConstructionService")
    Project = apps.get_model("construction", "Project")
    Testimonial = apps.get_model("construction", "Testimonial")
    Certification = apps.get_model("construction", "Certification")

    ConstructionService.objects.filter(
        slug__in=[s["slug"] for s in SERVICES]
    ).delete()
    Project.objects.filter(slug__in=[p["slug"] for p in PROJECTS]).delete()
    for t in TESTIMONIALS:
        Testimonial.objects.filter(
            author_name=t["author_name"], organisation=t["organisation"]
        ).delete()
    Certification.objects.filter(name__in=[c["name"] for c in CERTIFICATIONS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("construction", "0002_quoterequest_quoteattachment"),
    ]

    operations = [
        migrations.RunPython(seed_content, reverse_code=unseed_content),
    ]
