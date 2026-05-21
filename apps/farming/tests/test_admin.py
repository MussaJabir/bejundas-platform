import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from apps.farming.admin import OrderInquiryAdmin
from apps.farming.models import (
    Certification,
    Farm,
    FarmingProduct,
    OrderInquiry,
    Testimonial,
)


class TestAdminRegistration:
    """Every farming model is registered with Unfold's admin."""

    @pytest.mark.parametrize(
        "model",
        [FarmingProduct, Farm, Testimonial, Certification, OrderInquiry],
    )
    def test_model_registered(self, model):
        assert admin.site.is_registered(model)


@pytest.mark.django_db
class TestPillsRender:
    """Pill helpers return HTML — verify they don't crash and include the
    label text."""

    def test_product_category_pill(self, rf):
        p = FarmingProduct.objects.create(name="Maize", category="crops", summary="x")
        from apps.farming.admin import FarmingProductAdmin

        pill = FarmingProductAdmin(FarmingProduct, admin.site).category_pill(p)
        assert "Crops" in pill

    def test_inquiry_type_pill(self, rf):
        i = OrderInquiry.objects.create(
            full_name="X",
            email="x@example.com",
            phone="0712345678",
            products_of_interest="y",
            inquiry_type="partnership",
        )
        pill = OrderInquiryAdmin(OrderInquiry, admin.site).inquiry_type_pill(i)
        assert "Partnership" in pill

    def test_inquiry_status_pill(self, rf):
        i = OrderInquiry.objects.create(
            full_name="X",
            email="x@example.com",
            phone="0712345678",
            products_of_interest="y",
            status="fulfilled",
        )
        pill = OrderInquiryAdmin(OrderInquiry, admin.site).status_pill(i)
        assert "Fulfilled" in pill


@pytest.mark.django_db
class TestBulkActions:
    """5 bulk actions on OrderInquiry — each flips status on selected rows."""

    @pytest.fixture
    def inquiries(self):
        rows = [
            OrderInquiry.objects.create(
                full_name=f"Buyer {n}",
                email=f"b{n}@example.com",
                phone="0712345678",
                products_of_interest="x",
            )
            for n in range(3)
        ]
        return OrderInquiry.objects.filter(pk__in=[r.pk for r in rows])

    def _superuser_request(self):
        User = get_user_model()
        user = User.objects.create_superuser("admin", "admin@example.com", "p")
        req = RequestFactory().get("/")
        req.user = user
        # Required by admin's message_user
        from django.contrib.messages.storage.fallback import FallbackStorage

        req.session = {}
        req._messages = FallbackStorage(req)
        return req

    @pytest.mark.parametrize(
        "action,target",
        [
            ("mark_as_contacted", "contacted"),
            ("mark_as_quoted", "quoted"),
            ("mark_as_fulfilled", "fulfilled"),
            ("mark_as_declined", "declined"),
            ("mark_as_closed", "closed"),
        ],
    )
    def test_bulk_action_flips_status(self, inquiries, action, target):
        admin_instance = OrderInquiryAdmin(OrderInquiry, admin.site)
        req = self._superuser_request()
        getattr(admin_instance, action)(req, inquiries)
        for row in inquiries:
            row.refresh_from_db()
            assert row.status == target
