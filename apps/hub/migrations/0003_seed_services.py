from django.db import migrations

SERVICES = [
    {
        "title": "Financial Services",
        "slug": "financial-services",
        "summary": "Banking, insurance, and investment solutions for individuals and businesses across Tanzania.",
        "icon": "icon-Dollar",
        "url": "/financial/",
        "order": 1,
    },
    {
        "title": "Construction",
        "slug": "construction",
        "summary": "End-to-end construction and architectural solutions — from design to delivery — built to last.",
        "icon": "icon-Buildings",
        "url": "/construction/",
        "order": 2,
    },
    {
        "title": "Energies",
        "slug": "energies",
        "summary": "Sustainable energy systems and solutions powering homes and businesses toward a cleaner future.",
        "icon": "icon-Lightning",
        "url": "/energies/",
        "order": 3,
    },
    {
        "title": "Farming",
        "slug": "farming",
        "summary": "Modern agricultural solutions driving food security, rural growth, and sustainable land use.",
        "icon": "icon-Plant",
        "url": "/farming/",
        "order": 4,
    },
    {
        "title": "Investments",
        "slug": "investments",
        "summary": "Strategic investment advisory and portfolio management services for long-term wealth creation.",
        "icon": "icon-ChartLineUp",
        "url": "/investments/",
        "order": 5,
    },
]


def seed_services(apps, schema_editor):
    Service = apps.get_model("hub", "Service")
    for data in SERVICES:
        Service.objects.get_or_create(slug=data["slug"], defaults=data)


def unseed_services(apps, schema_editor):
    Service = apps.get_model("hub", "Service")
    slugs = [s["slug"] for s in SERVICES]
    Service.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("hub", "0002_service_url"),
    ]

    operations = [
        migrations.RunPython(seed_services, unseed_services),
    ]
