from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from apps.farming.models import (
    Certification,
    Farm,
    FarmingProduct,
    OrderInquiry,
    Testimonial,
)

# ── Shared pill helpers ─────────────────────────────────────────────


def _pill(label: str, bg: str, fg: str) -> str:
    return (
        f'<span style="background:{bg};color:{fg};font-size:11px;font-weight:700;'
        f"padding:2px 8px;border-radius:10px;text-transform:uppercase;"
        f'letter-spacing:.04em;">{label}</span>'
    )


def _status_pill(is_active: bool) -> str:
    if is_active:
        return _pill("Active", "#dcfce7", "#166534")
    return _pill("Inactive", "#f1f5f9", "#64748b")


def _featured_pill(is_featured: bool) -> str:
    if is_featured:
        return _pill("Featured", "#f1f8e9", "#3f6212")
    return _pill("Standard", "#f1f5f9", "#64748b")


# Forest-green / lime / earth-brown palette for categories.
_CATEGORY_COLOURS = {
    "crops": ("#dcfce7", "#166534"),  # leaf green
    "poultry": ("#fef3c7", "#a16207"),  # corn yellow
    "processed": ("#fee2e2", "#b91c1c"),  # brick red
}


_INQUIRY_TYPE_COLOURS = {
    "wholesale": ("#dbeafe", "#1d4ed8"),
    "retail": ("#fdf8e9", "#a98a35"),
    "partnership": ("#e0e7ff", "#4338ca"),
}


_INQUIRY_STATUS_COLOURS = {
    "new": ("#fee2e2", "#991b1b"),
    "contacted": ("#dbeafe", "#1d4ed8"),
    "quoted": ("#fef3c7", "#a16207"),
    "fulfilled": ("#dcfce7", "#166534"),
    "declined": ("#f1f5f9", "#64748b"),
    "closed": ("#e2e8f0", "#475569"),
}


# ── Admins ──────────────────────────────────────────────────────────


@admin.register(FarmingProduct)
class FarmingProductAdmin(ModelAdmin):
    list_display = [
        "product_thumbnail",
        "name",
        "category_pill",
        "unit",
        "order",
        "featured_pill",
        "status_pill",
    ]
    list_display_links = ["product_thumbnail", "name"]
    list_filter = ["category", "is_active", "is_featured", "unit"]
    search_fields = ["name", "summary", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 25
    ordering = ["order", "name"]
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "slug", "category", "summary", "description", "image"),
                "description": "Products shown on /farming/products/ and the homepage strip.",
            },
        ),
        (
            "Selling",
            {
                "fields": ("unit",),
                "description": "Default selling unit. No price is displayed on the site — "
                "buyers reach out for current pricing.",
            },
        ),
        (
            "Display",
            {
                "fields": ("is_active", "is_featured", "order"),
                "description": "Lower 'order' values appear first.",
            },
        ),
    )

    @admin.display(description="Photo")
    def product_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:48px;height:48px;border-radius:6px;object-fit:cover;'
                'border:1px solid #e2e8f0;" alt="">',
                obj.image.url,
            )
        return format_html(
            '<span style="display:inline-flex;width:48px;height:48px;border-radius:6px;'
            "background:#f1f8e9;color:#558b2f;align-items:center;justify-content:center;"
            'font-size:11px;border:1px solid #e2e8f0;">no photo</span>'
        )

    @admin.display(description="Category", ordering="category")
    def category_pill(self, obj):
        bg, fg = _CATEGORY_COLOURS.get(obj.category, ("#f1f5f9", "#64748b"))
        return format_html(_pill(obj.get_category_display(), bg, fg))

    @admin.display(description="Featured", ordering="is_featured")
    def featured_pill(self, obj):
        return format_html(_featured_pill(obj.is_featured))

    @admin.display(description="Status", ordering="is_active")
    def status_pill(self, obj):
        return format_html(_status_pill(obj.is_active))


@admin.register(Farm)
class FarmAdmin(ModelAdmin):
    list_display = [
        "farm_thumbnail",
        "name",
        "region",
        "activity_pill",
        "size_hectares",
        "order",
    ]
    list_display_links = ["farm_thumbnail", "name"]
    list_filter = ["primary_activity", "region"]
    search_fields = ["name", "region", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 25
    ordering = ["order", "name"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "region",
                    "size_hectares",
                    "primary_activity",
                    "description",
                    "cover_image",
                ),
                "description": "Physical farm locations shown on /farming/farms/.",
            },
        ),
        ("Display", {"fields": ("order",)}),
    )

    @admin.display(description="Cover")
    def farm_thumbnail(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width:60px;height:40px;border-radius:6px;object-fit:cover;'
                'border:1px solid #e2e8f0;" alt="">',
                obj.cover_image.url,
            )
        return format_html(
            '<span style="display:inline-flex;width:60px;height:40px;border-radius:6px;'
            "background:#f1f8e9;color:#558b2f;align-items:center;justify-content:center;"
            'font-size:11px;border:1px solid #e2e8f0;">no cover</span>'
        )

    @admin.display(description="Activity", ordering="primary_activity")
    def activity_pill(self, obj):
        bg, fg = _CATEGORY_COLOURS.get(obj.primary_activity, ("#f1f5f9", "#64748b"))
        return format_html(_pill(obj.get_primary_activity_display(), bg, fg))


@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ["author_name", "author_role", "organisation", "order", "featured_pill"]
    list_filter = ["is_featured"]
    search_fields = ["author_name", "organisation", "quote"]
    list_per_page = 25
    ordering = ["order", "-created_at"]
    fieldsets = (
        (
            None,
            {
                "fields": ("author_name", "author_role", "organisation", "quote"),
                "description": "Buyer / partner / cooperative quotes. Featured ones surface "
                "on the homepage.",
            },
        ),
        ("Display", {"fields": ("is_featured", "order")}),
    )

    @admin.display(description="Featured", ordering="is_featured")
    def featured_pill(self, obj):
        return format_html(_featured_pill(obj.is_featured))


@admin.register(Certification)
class CertificationAdmin(ModelAdmin):
    list_display = [
        "certificate_thumbnail",
        "name",
        "issuer",
        "reference_number",
        "year_awarded",
        "order",
        "status_pill",
    ]
    list_display_links = ["certificate_thumbnail", "name"]
    list_filter = ["is_active", "year_awarded"]
    search_fields = ["name", "issuer", "reference_number"]
    list_per_page = 25
    ordering = ["order", "-year_awarded"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "issuer",
                    "reference_number",
                    "year_awarded",
                    "certificate_image",
                ),
                "description": "Food-safety, TBS, organic, or other operating licences shown "
                "on the About page.",
            },
        ),
        ("Display", {"fields": ("is_active", "order")}),
    )

    @admin.display(description="Image")
    def certificate_thumbnail(self, obj):
        if obj.certificate_image:
            return format_html(
                '<img src="{}" style="width:48px;height:48px;border-radius:6px;object-fit:contain;'
                'background:#fff;border:1px solid #e2e8f0;padding:2px;" alt="">',
                obj.certificate_image.url,
            )
        return format_html(
            '<span style="display:inline-flex;width:48px;height:48px;border-radius:6px;'
            "background:#f1f8e9;color:#558b2f;align-items:center;justify-content:center;"
            'font-size:18px;border:1px solid #e2e8f0;">&#10003;</span>'
        )

    @admin.display(description="Status", ordering="is_active")
    def status_pill(self, obj):
        return format_html(_status_pill(obj.is_active))


@admin.register(OrderInquiry)
class OrderInquiryAdmin(ModelAdmin):
    list_display = [
        "submitted_label",
        "organisation_or_name",
        "inquiry_type_pill",
        "frequency",
        "delivery_location",
        "status_pill",
        "created_at",
    ]
    list_filter = ["status", "inquiry_type", "frequency", "preferred_contact", "created_at"]
    search_fields = [
        "full_name",
        "organisation",
        "email",
        "phone",
        "products_of_interest",
        "delivery_location",
    ]
    readonly_fields = [
        "full_name",
        "organisation",
        "email",
        "phone",
        "inquiry_type",
        "products_of_interest",
        "quantity",
        "frequency",
        "delivery_location",
        "preferred_contact",
        "notes",
        "created_at",
    ]
    list_per_page = 25
    actions = [
        "mark_as_contacted",
        "mark_as_quoted",
        "mark_as_fulfilled",
        "mark_as_declined",
        "mark_as_closed",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": ("status", "internal_notes"),
                "description": (
                    "Move the inquiry through the workflow: New → Contacted → "
                    "Quoted → Fulfilled / Declined / Closed."
                ),
            },
        ),
        (
            "Buyer",
            {
                "fields": (
                    "full_name",
                    "organisation",
                    "email",
                    "phone",
                    "preferred_contact",
                ),
                "description": "Submitted contact details (read-only).",
            },
        ),
        (
            "Order Details",
            {
                "fields": (
                    "inquiry_type",
                    "products_of_interest",
                    "quantity",
                    "frequency",
                    "delivery_location",
                ),
            },
        ),
        ("Notes", {"fields": ("notes",)}),
        ("Meta", {"fields": ("created_at",)}),
    )

    @admin.display(description="Submitted", ordering="-created_at")
    def submitted_label(self, obj):
        return obj.created_at.strftime("%d %b %Y")

    @admin.display(description="From")
    def organisation_or_name(self, obj):
        return obj.organisation or obj.full_name

    @admin.display(description="Type", ordering="inquiry_type")
    def inquiry_type_pill(self, obj):
        bg, fg = _INQUIRY_TYPE_COLOURS.get(obj.inquiry_type, ("#f1f5f9", "#64748b"))
        return format_html(_pill(obj.get_inquiry_type_display(), bg, fg))

    @admin.display(description="Status", ordering="status")
    def status_pill(self, obj):
        bg, fg = _INQUIRY_STATUS_COLOURS.get(obj.status, ("#f1f5f9", "#64748b"))
        return format_html(_pill(obj.get_status_display(), bg, fg))

    def _bulk_set_status(self, request, queryset, new_status, label):
        updated = queryset.update(status=new_status)
        self.message_user(
            request,
            f"{updated} order inquir{'ies' if updated != 1 else 'y'} marked as {label}.",
        )

    @admin.action(description="Mark selected as Contacted")
    def mark_as_contacted(self, request, queryset):
        self._bulk_set_status(request, queryset, "contacted", "contacted")

    @admin.action(description="Mark selected as Quoted")
    def mark_as_quoted(self, request, queryset):
        self._bulk_set_status(request, queryset, "quoted", "quoted")

    @admin.action(description="Mark selected as Fulfilled")
    def mark_as_fulfilled(self, request, queryset):
        self._bulk_set_status(request, queryset, "fulfilled", "fulfilled")

    @admin.action(description="Mark selected as Declined")
    def mark_as_declined(self, request, queryset):
        self._bulk_set_status(request, queryset, "declined", "declined")

    @admin.action(description="Mark selected as Closed")
    def mark_as_closed(self, request, queryset):
        self._bulk_set_status(request, queryset, "closed", "closed")
