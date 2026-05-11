from django.contrib import admin
from django.shortcuts import redirect
from unfold.admin import ModelAdmin

from apps.core.models import SiteSettings


class SiteSettingsProxyAdmin(ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return redirect("admin:core_sitesettings_change", SiteSettings.get().pk)


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        (
            "Identity",
            {
                "fields": (
                    "company_name",
                    "tagline",
                    "logo",
                    "favicon",
                )
            },
        ),
        (
            "About",
            {"fields": ("about_short",)},
        ),
        (
            "Contact",
            {"fields": ("phone", "email", "address")},
        ),
        (
            "Social Media",
            {"fields": ("facebook_url", "twitter_url", "linkedin_url", "instagram_url")},
        ),
    )
    list_display = ["company_name", "email", "phone"]
    search_fields = ["company_name", "email"]
