from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from apps.leads.models import Lead, VerticalPlaceholder


@admin.register(VerticalPlaceholder)
class VerticalPlaceholderAdmin(ModelAdmin):
    list_display = ["vertical", "headline", "color_swatch", "status_pill"]
    list_filter = ["vertical", "is_active"]
    search_fields = ["vertical", "headline"]
    list_per_page = 20
    ordering = ["vertical"]
    fieldsets = (
        (
            None,
            {
                "fields": ("vertical", "is_active"),
                "description": "Each vertical has its own Coming Soon page themed by the colors below.",
            },
        ),
        (
            "Content",
            {
                "fields": ("headline", "subheadline"),
                "description": "Headline and subheadline shown on the Coming Soon page for this vertical.",
            },
        ),
        (
            "Theme",
            {
                "fields": ("primary_color", "accent_color"),
                "description": "Hex colors (e.g. #1a1a2e) applied to this vertical's Coming Soon page.",
            },
        ),
    )

    @admin.display(description="Theme", ordering="primary_color")
    def color_swatch(self, obj):
        return format_html(
            '<span style="display:inline-block;width:16px;height:16px;border-radius:50%;'
            'background:{};border:1px solid #00000020;vertical-align:middle;margin-right:6px;"></span>'
            '<span style="display:inline-block;width:16px;height:16px;border-radius:50%;'
            'background:{};border:1px solid #00000020;vertical-align:middle;"></span>',
            obj.primary_color,
            obj.accent_color,
        )

    @admin.display(description="Status", ordering="is_active")
    def status_pill(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background:#dcfce7;color:#166534;font-size:11px;font-weight:700;'
                'padding:2px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em;">Active</span>'
            )
        return format_html(
            '<span style="background:#f1f5f9;color:#64748b;font-size:11px;font-weight:700;'
            'padding:2px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em;">Inactive</span>'
        )


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = ["name", "email", "vertical", "status_pill", "created_at"]
    list_filter = ["vertical", "notified", "created_at"]
    search_fields = ["name", "email", "phone", "message"]
    readonly_fields = ["name", "email", "phone", "message", "vertical", "created_at"]
    list_per_page = 25
    actions = ["mark_as_notified", "mark_as_unread"]
    fieldsets = (
        (
            None,
            {
                "fields": ("vertical", "name", "email", "phone"),
                "description": "Submitted via the Coming Soon form for this vertical. Read-only.",
            },
        ),
        ("Message", {"fields": ("message",)}),
        (
            "Status",
            {
                "fields": ("notified", "created_at"),
                "description": "Tick 'notified' once you have followed up with this lead.",
            },
        ),
    )

    @admin.display(description="Status", ordering="notified")
    def status_pill(self, obj):
        if obj.notified:
            return format_html(
                '<span style="background:#dcfce7;color:#166534;font-size:11px;font-weight:700;'
                'padding:2px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em;">Notified</span>'
            )
        return format_html(
            '<span style="background:#fee2e2;color:#991b1b;font-size:11px;font-weight:700;'
            'padding:2px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em;">New</span>'
        )

    @admin.action(description="Mark selected leads as notified")
    def mark_as_notified(self, request, queryset):
        updated = queryset.update(notified=True)
        self.message_user(
            request, f"{updated} lead{'s' if updated != 1 else ''} marked as notified."
        )

    @admin.action(description="Mark selected leads as unread (new)")
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(notified=False)
        self.message_user(request, f"{updated} lead{'s' if updated != 1 else ''} marked as unread.")
