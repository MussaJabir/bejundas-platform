from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from apps.hub.models import News, Service, TeamMember


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


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ["title", "icon_chip", "order", "status_pill"]
    list_filter = ["is_active"]
    search_fields = ["title", "summary"]
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 20
    ordering = ["order", "title"]
    fieldsets = (
        (
            None,
            {
                "fields": ("title", "slug", "summary", "icon", "url", "order", "is_active"),
                "description": "Services shown in the home page services section and on /services/.",
            },
        ),
    )

    @admin.display(description="Icon", ordering="icon")
    def icon_chip(self, obj):
        if not obj.icon:
            return "—"
        return format_html(
            '<code style="font-family:monospace;font-size:11px;background:#dbeafe;color:#1d4ed8;'
            'padding:2px 8px;border-radius:4px;">{}</code>',
            obj.icon,
        )

    @admin.display(description="Status", ordering="is_active")
    def status_pill(self, obj):
        return format_html(_status_pill(obj.is_active))


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ["photo_thumbnail", "name", "role", "order", "status_pill"]
    list_display_links = ["photo_thumbnail", "name"]
    list_filter = ["is_active"]
    search_fields = ["name", "role"]
    list_per_page = 25
    ordering = ["order", "name"]
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "role", "bio", "photo", "order", "is_active"),
                "description": "Members shown on the Team page. Square photos look best.",
            },
        ),
    )

    @admin.display(description="Photo")
    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width:36px;height:36px;border-radius:50%;object-fit:cover;'
                'border:1px solid #e2e8f0;" alt="">',
                obj.photo.url,
            )
        return format_html(
            '<span style="display:inline-flex;width:36px;height:36px;border-radius:50%;'
            "background:#f1f5f9;color:#94a3b8;align-items:center;justify-content:center;"
            'font-weight:700;font-size:14px;border:1px solid #e2e8f0;">{}</span>',
            (obj.name[:1] if obj.name else "?").upper(),
        )

    @admin.display(description="Status", ordering="is_active")
    def status_pill(self, obj):
        return format_html(_status_pill(obj.is_active))


@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ["cover_thumbnail", "title", "published_pill", "published_at"]
    list_display_links = ["cover_thumbnail", "title"]
    list_filter = ["published", "published_at"]
    search_fields = ["title", "excerpt", "body"]
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 20
    ordering = ["-published_at", "-created_at"]
    fieldsets = (
        (
            None,
            {
                "fields": ("title", "slug", "excerpt", "body", "cover"),
                "description": "Articles shown on /news/. Excerpt appears in the listing; body on the detail page.",
            },
        ),
        (
            "Publishing",
            {
                "fields": ("published", "published_at"),
                "description": "Articles only appear publicly when published is ticked AND published_at is set in the past.",
            },
        ),
    )

    @admin.display(description="Cover")
    def cover_thumbnail(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="width:60px;height:40px;border-radius:6px;object-fit:cover;'
                'border:1px solid #e2e8f0;" alt="">',
                obj.cover.url,
            )
        return format_html(
            '<span style="display:inline-flex;width:60px;height:40px;border-radius:6px;'
            "background:#f1f5f9;color:#94a3b8;align-items:center;justify-content:center;"
            'font-size:11px;border:1px solid #e2e8f0;">no cover</span>'
        )

    @admin.display(description="Published", ordering="published")
    def published_pill(self, obj):
        if obj.published:
            return format_html(
                '<span style="background:#dcfce7;color:#166534;font-size:11px;font-weight:700;'
                'padding:2px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em;">Live</span>'
            )
        return format_html(
            '<span style="background:#fef3c7;color:#a16207;font-size:11px;font-weight:700;'
            'padding:2px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em;">Draft</span>'
        )
