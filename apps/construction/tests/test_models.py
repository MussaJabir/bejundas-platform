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
            name="Residential Builds", summary="Custom homes and villas."
        )
        assert str(svc) == "Residential Builds"

    def test_slug_auto_filled(self):
        svc = ConstructionService.objects.create(
            name="Civil Works", summary="Heavy civil engineering."
        )
        assert svc.slug == "civil-works"

    def test_default_is_active(self):
        svc = ConstructionService.objects.create(name="MEP", summary="MEP installs.")
        assert svc.is_active is True

    def test_default_ordering(self):
        ConstructionService.objects.create(name="A", summary="x", order=2)
        ConstructionService.objects.create(name="B", summary="x", order=1)
        names = list(ConstructionService.objects.values_list("name", flat=True))
        assert names == ["B", "A"]


@pytest.mark.django_db
class TestProject:
    def test_str_includes_year(self):
        p = Project.objects.create(
            title="Masaki Tower",
            sector="residential",
            location_city="Dar es Salaam",
            year_completed=2024,
        )
        assert str(p) == "Masaki Tower (2024)"

    def test_slug_auto_filled(self):
        p = Project.objects.create(
            title="Dodoma Logistics Hub",
            sector="industrial",
            location_city="Dodoma",
            year_completed=2023,
        )
        assert p.slug == "dodoma-logistics-hub"

    def test_sector_choices_enforced(self):
        # Django doesn't enforce at DB level, but get_sector_display() relies on choices
        p = Project.objects.create(
            title="Ring Road",
            sector="civil",
            location_city="Mwanza",
            year_completed=2022,
        )
        assert p.get_sector_display() == "Civil Works"

    def test_default_not_featured(self):
        p = Project.objects.create(
            title="X",
            sector="commercial",
            location_city="Arusha",
            year_completed=2025,
        )
        assert p.is_featured is False


@pytest.mark.django_db
class TestTestimonial:
    def test_str_with_organisation(self):
        t = Testimonial.objects.create(
            author_name="Amina Hassan",
            organisation="Hassan Holdings",
            quote="Outstanding delivery.",
        )
        assert str(t) == "Amina Hassan — Hassan Holdings"

    def test_str_without_organisation(self):
        t = Testimonial.objects.create(author_name="John Doe", quote="Great team.")
        assert str(t) == "John Doe"

    def test_default_not_featured(self):
        t = Testimonial.objects.create(author_name="X", quote="y")
        assert t.is_featured is False


@pytest.mark.django_db
class TestCertification:
    def test_str(self):
        c = Certification.objects.create(name="ISO 9001", issuer="ISO", year_awarded=2023)
        assert str(c) == "ISO 9001 (ISO)"

    def test_default_is_active(self):
        c = Certification.objects.create(name="NCC Class 1", issuer="NCC", year_awarded=2024)
        assert c.is_active is True
