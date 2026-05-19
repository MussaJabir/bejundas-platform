from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from apps.construction.models import (
    Certification,
    ConstructionService,
    Project,
    Testimonial,
)

# ── Shared pill helpers ─────────────────────────────────────────────


def _status_pill(is_active: bool) -> str:
    if is_active:
        return (
            '<span style="background:#dcfce7;color:#166534;font-size:11px;font-weight:700;'
            'padding:2px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em;">Active</span>'
        )
    return (
        '<span style="background:#f1f5f9;color:#64748b;font-size:11px;font-weight:700;'
        'padding:2px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em;">Inactive</span>'
    )


def _featured_pill(is_featured: bool) -> str:
    if is_featured:
        return (
            '<span style="background:#fff4ec;color:#c2410c;font-size:11px;font-weight:700;'
            'padding:2px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em;">Featured</span>'
        )
    return (
        '<span style="background:#f1f5f9;color:#64748b;font-size:11px;font-weight:700;'
        'padding:2px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em;">Standard</span>'
    )


# Sector pill colour map — keeps the construction palette consistent.
_SECTOR_COLOURS = {
    "residential": ("#dbeafe", "#1d4ed8"),
    "commercial": ("#fef3c7", "#a16207"),
    "civil": ("#fee2e2", "#b91c1c"),
    "industrial": ("#e0e7ff", "#4338ca"),
    "fitout": ("#fff4ec", "#c2410c"),
    "renovation": ("#dcfce7", "#166534"),
}


# ── Admins ──────────────────────────────────────────────────────────


@admin.register(ConstructionService)
class ConstructionServiceAdmin(ModelAdmin):
    list_display = ["name", "icon_chip", "order", "status_pill"]
    list_filter = ["is_active"]
    search_fields = ["name", "summary", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 20
    ordering = ["order", "name"]
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "slug", "summary", "description", "icon"),
                "description": (
                    "Construction services shown on the /construction/services/ page "
                    "and as preview cards on the homepage."
                ),
            },
        ),
        (
            "Display",
            {
                "fields": ("order", "is_active"),
                "description": "Lower 'order' values appear first.",
            },
        ),
    )

    @admin.display(description="Icon", ordering="icon")
    def icon_chip(self, obj):
        if not obj.icon:
            return "—"
        return format_html(
            '<code style="font-family:monospace;font-size:11px;background:#fff4ec;color:#c2410c;'
            'padding:2px 8px;border-radius:4px;">{}</code>',
            obj.icon,
        )

    @admin.display(description="Status", ordering="is_active")
    def status_pill(self, obj):
        return format_html(_status_pill(obj.is_active))


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = [
        "cover_thumbnail",
        "title",
        "sector_pill",
        "location_city",
        "year_completed",
        "featured_pill",
    ]
    list_display_links = ["cover_thumbnail", "title"]
    list_filter = ["sector", "is_featured", "year_completed"]
    search_fields = ["title", "description", "location_city", "location_region"]
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 25
    ordering = ["order", "-year_completed"]
    fieldsets = (
        (
            None,
            {
                "fields": ("title", "slug", "sector", "description", "cover_image"),
                "description": "Project portfolio entry shown on /construction/projects/.",
            },
        ),
        (
            "Location & Timing",
            {
                "fields": ("location_city", "location_region", "year_completed"),
            },
        ),
        (
            "Display",
            {
                "fields": ("is_featured", "order"),
                "description": "Featured projects appear in the homepage 'Featured Projects' strip.",
            },
        ),
    )

    @admin.display(description="Cover")
    def cover_thumbnail(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width:60px;height:40px;border-radius:6px;object-fit:cover;'
                'border:1px solid #e2e8f0;" alt="">',
                obj.cover_image.url,
            )
        return format_html(
            '<span style="display:inline-flex;width:60px;height:40px;border-radius:6px;'
            "background:#f1f5f9;color:#94a3b8;align-items:center;justify-content:center;"
            'font-size:11px;border:1px solid #e2e8f0;">no cover</span>'
        )

    @admin.display(description="Sector", ordering="sector")
    def sector_pill(self, obj):
        bg, fg = _SECTOR_COLOURS.get(obj.sector, ("#f1f5f9", "#64748b"))
        return format_html(
            '<span style="background:{};color:{};font-size:11px;font-weight:700;'
            'padding:2px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em;">{}</span>',
            bg,
            fg,
            obj.get_sector_display(),
        )

    @admin.display(description="Featured", ordering="is_featured")
    def featured_pill(self, obj):
        return format_html(_featured_pill(obj.is_featured))


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
                "description": "Client testimonials. Featured ones surface on the homepage.",
            },
        ),
        (
            "Display",
            {"fields": ("is_featured", "order")},
        ),
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
        "year_awarded",
        "order",
        "status_pill",
    ]
    list_display_links = ["certificate_thumbnail", "name"]
    list_filter = ["is_active", "year_awarded"]
    search_fields = ["name", "issuer"]
    list_per_page = 25
    ordering = ["order", "-year_awarded"]
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "issuer", "year_awarded", "certificate_image"),
                "description": "Certifications and licences shown on the About page.",
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
            "background:#f1f5f9;color:#94a3b8;align-items:center;justify-content:center;"
            'font-size:18px;border:1px solid #e2e8f0;">&#10003;</span>'
        )

    @admin.display(description="Status", ordering="is_active")
    def status_pill(self, obj):
        return format_html(_status_pill(obj.is_active))
