from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.leads.models import Lead, VerticalPlaceholder


@admin.register(VerticalPlaceholder)
class VerticalPlaceholderAdmin(ModelAdmin):
    list_display = ["vertical", "headline", "is_active"]
    list_filter = ["vertical", "is_active"]
    search_fields = ["vertical", "headline"]
    fieldsets = (
        (None, {"fields": ("vertical", "is_active")}),
        ("Content", {"fields": ("headline", "subheadline")}),
        ("Theme", {"fields": ("primary_color", "accent_color")}),
    )


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = ["name", "email", "vertical", "notified", "created_at"]
    list_filter = ["vertical", "notified"]
    search_fields = ["name", "email", "phone"]
    readonly_fields = ["name", "email", "phone", "message", "vertical", "created_at"]
    fieldsets = (
        (None, {"fields": ("vertical", "name", "email", "phone")}),
        ("Message", {"fields": ("message",)}),
        ("Status", {"fields": ("notified", "created_at")}),
    )
