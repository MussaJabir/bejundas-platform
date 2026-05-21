from decimal import Decimal

import pytest

from apps.farming.models import (
    FREQUENCY_CHOICES,
    INQUIRY_STATUS_CHOICES,
    INQUIRY_TYPE_CHOICES,
    PRODUCT_CATEGORY_CHOICES,
    UNIT_CHOICES,
    Certification,
    Farm,
    FarmingProduct,
    OrderInquiry,
    Testimonial,
)


@pytest.mark.django_db
class TestFarmingProduct:
    def test_str_returns_name(self):
        p = FarmingProduct.objects.create(
            name="Sukuma Wiki", category="crops", summary="Leafy greens."
        )
        assert str(p) == "Sukuma Wiki"

    def test_slug_auto_populates_from_name(self):
        p = FarmingProduct.objects.create(name="Layer Eggs", category="poultry", summary="Trays.")
        assert p.slug == "layer-eggs"

    def test_explicit_slug_preserved(self):
        p = FarmingProduct.objects.create(
            name="Sunflower Oil", slug="sunflower-oil-1l", category="processed", summary="1L"
        )
        assert p.slug == "sunflower-oil-1l"

    def test_defaults(self):
        p = FarmingProduct.objects.create(name="Maize", category="crops", summary="x")
        assert p.unit == "kg"
        assert p.is_active is True
        assert p.is_featured is False
        assert p.order == 0
        assert p.description == ""

    def test_ordering_by_order_then_name(self):
        FarmingProduct.objects.create(name="Zebra Beans", category="crops", summary="x", order=10)
        FarmingProduct.objects.create(name="Beans", category="crops", summary="x", order=1)
        FarmingProduct.objects.create(name="Apple", category="crops", summary="x", order=1)
        assert [p.name for p in FarmingProduct.objects.all()] == [
            "Apple",
            "Beans",
            "Zebra Beans",
        ]


@pytest.mark.django_db
class TestFarm:
    def test_str_includes_region(self):
        f = Farm.objects.create(
            name="Mbeya Highland Farm", region="Mbeya", primary_activity="crops"
        )
        assert str(f) == "Mbeya Highland Farm (Mbeya)"

    def test_slug_auto_populates(self):
        f = Farm.objects.create(
            name="Coast Region Poultry Farm", region="Pwani", primary_activity="poultry"
        )
        assert f.slug == "coast-region-poultry-farm"

    def test_get_absolute_url_uses_anchor(self):
        f = Farm.objects.create(
            name="Mbeya Highland Farm", region="Mbeya", primary_activity="crops"
        )
        assert f.get_absolute_url() == "/farming/farms/#mbeya-highland-farm"

    def test_size_hectares_optional(self):
        f = Farm.objects.create(name="Tiny Plot", region="Dar", primary_activity="poultry")
        assert f.size_hectares is None

    def test_size_hectares_accepts_decimal(self):
        f = Farm.objects.create(
            name="Big Farm",
            region="Iringa",
            primary_activity="crops",
            size_hectares=Decimal("125.50"),
        )
        assert f.size_hectares == Decimal("125.50")


@pytest.mark.django_db
class TestTestimonial:
    def test_str_with_org(self):
        t = Testimonial.objects.create(
            author_name="Mama Mwajuma", organisation="Mwajuma Wholesale", quote="x"
        )
        assert str(t) == "Mama Mwajuma — Mwajuma Wholesale"

    def test_str_without_org(self):
        t = Testimonial.objects.create(author_name="Solo Buyer", quote="x")
        assert str(t) == "Solo Buyer"

    def test_defaults(self):
        t = Testimonial.objects.create(author_name="X", quote="y")
        assert t.is_featured is False
        assert t.order == 0
        assert t.author_role == ""
        assert t.organisation == ""


@pytest.mark.django_db
class TestCertification:
    def test_str_includes_issuer(self):
        c = Certification.objects.create(
            name="TBS Food Safety Mark", issuer="Tanzania Bureau of Standards"
        )
        assert str(c) == "TBS Food Safety Mark (Tanzania Bureau of Standards)"

    def test_defaults(self):
        c = Certification.objects.create(name="X", issuer="Y")
        assert c.is_active is True
        assert c.order == 0
        assert c.reference_number == ""
        assert c.year_awarded is None


@pytest.mark.django_db
class TestOrderInquiry:
    def _create(self, **kwargs):
        defaults = {
            "full_name": "Asha Buyer",
            "email": "asha@example.com",
            "phone": "+255712345678",
            "products_of_interest": "Eggs, broilers",
        }
        defaults.update(kwargs)
        return OrderInquiry.objects.create(**defaults)

    def test_str_uses_organisation_when_present(self):
        i = self._create(organisation="Asha Trading", inquiry_type="wholesale")
        assert "Asha Trading" in str(i)
        assert "Wholesale Buyer" in str(i)
        assert "New" in str(i)

    def test_str_falls_back_to_name(self):
        i = self._create(inquiry_type="retail")
        assert "Asha Buyer" in str(i)
        assert "Retail Customer" in str(i)

    def test_defaults(self):
        i = self._create()
        assert i.status == "new"
        assert i.inquiry_type == "wholesale"
        assert i.frequency == "one_off"
        assert i.preferred_contact == "phone"
        assert i.organisation == ""
        assert i.notes == ""
        assert i.internal_notes == ""

    def test_ordering_by_created_desc(self):
        a = self._create(full_name="First")
        b = self._create(full_name="Second")
        names = list(OrderInquiry.objects.values_list("full_name", flat=True))
        # Most recent first
        assert names[0] == b.full_name
        assert names[1] == a.full_name


class TestChoiceCatalogues:
    """Locks the choice tuples so a typo in models.py is caught immediately."""

    def test_product_category_codes(self):
        codes = {c for c, _ in PRODUCT_CATEGORY_CHOICES}
        assert codes == {"crops", "poultry", "processed"}

    def test_unit_codes(self):
        codes = {c for c, _ in UNIT_CHOICES}
        assert {"kg", "dozen", "each", "litre", "bag"} <= codes

    def test_inquiry_type_codes(self):
        codes = {c for c, _ in INQUIRY_TYPE_CHOICES}
        assert codes == {"wholesale", "retail", "partnership"}

    def test_frequency_codes(self):
        codes = {c for c, _ in FREQUENCY_CHOICES}
        assert codes == {"one_off", "monthly", "seasonal"}

    def test_inquiry_status_six_state_workflow(self):
        codes = [c for c, _ in INQUIRY_STATUS_CHOICES]
        assert codes == ["new", "contacted", "quoted", "fulfilled", "declined", "closed"]
