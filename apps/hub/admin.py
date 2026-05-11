from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.hub.models import News, Service, TeamMember


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ["title", "order", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["title", "summary"]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = ((None, {"fields": ("title", "slug", "summary", "icon", "order", "is_active")}),)


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ["name", "role", "order", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "role"]
    fieldsets = ((None, {"fields": ("name", "role", "bio", "photo", "order", "is_active")}),)


@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ["title", "published", "published_at"]
    list_filter = ["published"]
    search_fields = ["title", "excerpt", "body"]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "excerpt", "body", "cover")}),
        ("Publishing", {"fields": ("published", "published_at")}),
    )
