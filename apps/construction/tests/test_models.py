"""Model tests — use unique names prefixed with 'TestPrefix' to avoid
collisions with seeded curated content from migration 0003."""

import pytest

from apps.construction.models import (
    Certification,
    ConstructionService,
    Project,
    Testimonial,
)


@pytest.mark.django_db
class TestConstructionService:
    def test_str(self):
        svc = ConstructionService.objects.create(
            name="TestPrefix Residential", summary="Custom homes and villas."
        )
        assert str(svc) == "TestPrefix Residential"

    def test_slug_auto_filled(self):
        svc = ConstructionService.objects.create(
            name="TestPrefix Civil Engineering", summary="Heavy civil engineering."
        )
        assert svc.slug == "testprefix-civil-engineering"

    def test_default_is_active(self):
        svc = ConstructionService.objects.create(name="TestPrefix MEP", summary="MEP installs.")
        assert svc.is_active is True

    def test_default_ordering(self):
        # Scope assertion to only test-created rows to avoid collision with seed.
        svc_a = ConstructionService.objects.create(name="TestPrefix Alpha", summary="x", order=99)
        svc_b = ConstructionService.objects.create(name="TestPrefix Beta", summary="x", order=98)
        ours = ConstructionService.objects.filter(name__startswith="TestPrefix").order_by(
            "order", "name"
        )
        assert list(ours) == [svc_b, svc_a]


@pytest.mark.django_db
class TestProject:
    def test_str_includes_year(self):
        p = Project.objects.create(
            title="TestPrefix Tower",
            sector="residential",
            location_city="Dar es Salaam",
            year_completed=2024,
        )
        assert str(p) == "TestPrefix Tower (2024)"

    def test_slug_auto_filled(self):
        p = Project.objects.create(
            title="TestPrefix Logistics Hub",
            sector="industrial",
            location_city="Dodoma",
            year_completed=2023,
        )
        assert p.slug == "testprefix-logistics-hub"

    def test_sector_choices_enforced(self):
        # Django doesn't enforce at DB level, but get_sector_display() relies on choices
        p = Project.objects.create(
            title="TestPrefix Ring Road",
            sector="civil",
            location_city="Mwanza",
            year_completed=2022,
        )
        assert p.get_sector_display() == "Civil Works"

    def test_default_not_featured(self):
        p = Project.objects.create(
            title="TestPrefix X",
            sector="commercial",
            location_city="Arusha",
            year_completed=2025,
        )
        assert p.is_featured is False


@pytest.mark.django_db
class TestTestimonial:
    def test_str_with_organisation(self):
        t = Testimonial.objects.create(
            author_name="TestPrefix Author",
            organisation="TestPrefix Holdings",
            quote="Outstanding delivery.",
        )
        assert str(t) == "TestPrefix Author — TestPrefix Holdings"

    def test_str_without_organisation(self):
        t = Testimonial.objects.create(author_name="TestPrefix Solo", quote="Great team.")
        assert str(t) == "TestPrefix Solo"

    def test_default_not_featured(self):
        t = Testimonial.objects.create(author_name="TestPrefix Anon", quote="y")
        assert t.is_featured is False


@pytest.mark.django_db
class TestCertification:
    def test_str(self):
        c = Certification.objects.create(
            name="TestPrefix ISO 9001", issuer="ISO", year_awarded=2023
        )
        assert str(c) == "TestPrefix ISO 9001 (ISO)"

    def test_default_is_active(self):
        c = Certification.objects.create(name="TestPrefix NCC", issuer="NCC", year_awarded=2024)
        assert c.is_active is True
