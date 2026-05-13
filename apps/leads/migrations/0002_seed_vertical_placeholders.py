import uuid

from django.db import migrations
from django.utils import timezone

PLACEHOLDERS = [
    {
        "vertical": "financial",
        "headline": "World-Class Financial Services. Coming Soon.",
        "subheadline": "Bejundas Financial is building innovative, trustworthy financial solutions for individuals and businesses across East Africa. Be the first to know when we launch.",
        "primary_color": "#0a2342",
        "accent_color": "#c9a84c",
    },
    {
        "vertical": "construction",
        "headline": "Building the Future. Coming Soon.",
        "subheadline": "Bejundas Construction delivers premium commercial and residential projects built to last. Leave your details and we will reach out when we open for enquiries.",
        "primary_color": "#2c2c2c",
        "accent_color": "#f47920",
    },
    {
        "vertical": "energies",
        "headline": "Clean Energy Solutions. Coming Soon.",
        "subheadline": "Bejundas Energies is bringing sustainable, reliable energy solutions to Tanzania and the region. Sign up to be notified at launch.",
        "primary_color": "#0d3b2e",
        "accent_color": "#f9c41a",
    },
    {
        "vertical": "farming",
        "headline": "Modern Agriculture. Coming Soon.",
        "subheadline": "Bejundas Farming is transforming agricultural production with modern methods and technology. Register your interest today.",
        "primary_color": "#2d5a27",
        "accent_color": "#8bc34a",
    },
    {
        "vertical": "investments",
        "headline": "Strategic Investments. Coming Soon.",
        "subheadline": "Bejundas Investments provides high-quality investment opportunities for growth-focused individuals and institutions. Join our early interest list.",
        "primary_color": "#1a0533",
        "accent_color": "#d4af37",
    },
]


def seed_placeholders(apps, schema_editor):
    VerticalPlaceholder = apps.get_model("leads", "VerticalPlaceholder")
    now = timezone.now()
    for data in PLACEHOLDERS:
        VerticalPlaceholder.objects.get_or_create(
            vertical=data["vertical"],
            defaults={
                "id": uuid.uuid4(),
                "headline": data["headline"],
                "subheadline": data["subheadline"],
                "primary_color": data["primary_color"],
                "accent_color": data["accent_color"],
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
        )


def unseed_placeholders(apps, schema_editor):
    VerticalPlaceholder = apps.get_model("leads", "VerticalPlaceholder")
    verticals = [p["vertical"] for p in PLACEHOLDERS]
    VerticalPlaceholder.objects.filter(vertical__in=verticals).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_placeholders, reverse_code=unseed_placeholders),
    ]
