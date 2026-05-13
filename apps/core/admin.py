from django.contrib import admin
from django.shortcuts import redirect
from unfold.admin import ModelAdmin

from apps.core.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return redirect("admin:core_sitesettings_change", SiteSettings.get().pk)

    fieldsets = (
        (
            "Identity",
            {"fields": ("company_name", "tagline", "logo", "favicon")},
        ),
        (
            "Hero Section",
            {"fields": ("hero_headline", "hero_subheadline", "hero_cta_text")},
        ),
        (
            "About Section",
            {
                "fields": (
                    "about_headline",
                    "about_body",
                    "about_video_url",
                    "years_experience",
                    "projects_count",
                    "clients_count",
                    "satisfaction_pct",
                )
            },
        ),
        (
            "Mission & Vision",
            {"fields": ("mission", "vision")},
        ),
        (
            "CTA Section",
            {"fields": ("cta_headline", "cta_body")},
        ),
        (
            "Contact",
            {"fields": ("phone", "email", "address", "about_short")},
        ),
        (
            "Social Media",
            {"fields": ("facebook_url", "twitter_url", "linkedin_url", "instagram_url")},
        ),
    )
    list_display = ["company_name", "email", "phone"]
    search_fields = ["company_name", "email"]
