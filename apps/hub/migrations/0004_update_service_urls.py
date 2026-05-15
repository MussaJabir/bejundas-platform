from django.db import migrations

NEW_URLS = {
    "financial-services": "/financial/",
    "construction": "/construction/",
    "energies": "/energies/",
    "farming": "/farming/",
    "investments": "/investments/",
}

OLD_URLS = {
    "financial-services": "https://financial.bejundas.co.tz",
    "construction": "https://construction.bejundas.co.tz",
    "energies": "https://energies.bejundas.co.tz",
    "farming": "https://farming.bejundas.co.tz",
    "investments": "https://investments.bejundas.co.tz",
}


def forwards(apps, schema_editor):
    Service = apps.get_model("hub", "Service")
    for slug, url in NEW_URLS.items():
        Service.objects.filter(slug=slug).update(url=url)


def backwards(apps, schema_editor):
    Service = apps.get_model("hub", "Service")
    for slug, url in OLD_URLS.items():
        Service.objects.filter(slug=slug).update(url=url)


class Migration(migrations.Migration):

    dependencies = [
        ("hub", "0003_seed_services"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
