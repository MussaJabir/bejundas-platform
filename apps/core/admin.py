from datetime import timedelta

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from unfold.admin import ModelAdmin

from apps.core.models import (
    AboutSettings,
    ContactSettings,
    CTASettings,
    HeroSettings,
    IdentitySettings,
    MissionVisionSettings,
    SiteSettings,
    SocialMediaSettings,
)


def unread_leads_badge(request):
    from apps.leads.models import Lead

    count = Lead.objects.filter(notified=False).count()
    return str(count) if count else None


def dashboard_callback(request, context):
    from apps.hub.models import News, Service, TeamMember
    from apps.leads.models import Lead, VerticalPlaceholder

    week_ago = timezone.now() - timedelta(days=7)
    total_leads = Lead.objects.count()
    new_this_week = Lead.objects.filter(created_at__gte=week_ago).count()
    unread_leads = Lead.objects.filter(notified=False).count()
    notified_leads = Lead.objects.filter(notified=True).count()

    leads_by_vertical = []
    for placeholder in VerticalPlaceholder.objects.order_by("vertical"):
        count = Lead.objects.filter(vertical=placeholder.vertical).count()
        leads_by_vertical.append(
            {
                "vertical": placeholder.vertical,
                "label": placeholder.vertical.title(),
                "count": count,
                "primary_color": placeholder.primary_color,
                "is_active": placeholder.is_active,
            }
        )
    max_vertical_count = max((v["count"] for v in leads_by_vertical), default=0)

    context.update(
        {
            "total_leads": total_leads,
            "new_this_week": new_this_week,
            "unread_leads": unread_leads,
            "notified_leads": notified_leads,
            "active_verticals": VerticalPlaceholder.objects.filter(is_active=True).count(),
            "verticals_total": VerticalPlaceholder.objects.count(),
            "services_count": Service.objects.filter(is_active=True).count(),
            "news_count": News.objects.filter(published=True).count(),
            "team_count": TeamMember.objects.filter(is_active=True).count(),
            "leads_by_vertical": leads_by_vertical,
            "max_vertical_count": max_vertical_count,
            "recent_leads": Lead.objects.order_by("-created_at")[:6],
        }
    )
    return context


class _BaseSiteSettingsAdmin(ModelAdmin):
    """Shared base for all SiteSettings proxy admins.

    The underlying SiteSettings is a singleton row, so add and delete are
    disabled, and the changelist view redirects straight to the change
    form for that single row.
    """

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        model_name = self.model._meta.model_name
        singleton_pk = SiteSettings.get().pk
        return HttpResponseRedirect(reverse(f"admin:core_{model_name}_change", args=[singleton_pk]))


@admin.register(IdentitySettings)
class IdentitySettingsAdmin(_BaseSiteSettingsAdmin):
    fieldsets = (
        (
            "Identity & Branding",
            {
                "fields": ("company_name", "tagline", "logo", "favicon"),
                "description": "Brand name, tagline, and uploaded logo / favicon images.",
            },
        ),
    )


@admin.register(HeroSettings)
class HeroSettingsAdmin(_BaseSiteSettingsAdmin):
    fieldsets = (
        (
            "Home Page — Hero Section",
            {
                "fields": ("hero_headline", "hero_subheadline", "hero_cta_text"),
                "description": "The main banner shown at the top of the home page.",
            },
        ),
    )


@admin.register(AboutSettings)
class AboutSettingsAdmin(_BaseSiteSettingsAdmin):
    fieldsets = (
        (
            "About",
            {
                "fields": ("about_headline", "about_body", "about_short", "about_video_url"),
                "description": "About section content shown on Home and About pages.",
            },
        ),
        (
            "Stats Counters",
            {
                "fields": (
                    "years_experience",
                    "projects_count",
                    "clients_count",
                    "satisfaction_pct",
                ),
                "description": "Numbers shown on the About page counter strip.",
            },
        ),
    )


@admin.register(MissionVisionSettings)
class MissionVisionSettingsAdmin(_BaseSiteSettingsAdmin):
    fieldsets = (
        (
            "Mission & Vision",
            {
                "fields": ("mission", "vision"),
                "description": "Shown on the About page below the company introduction.",
            },
        ),
    )


@admin.register(CTASettings)
class CTASettingsAdmin(_BaseSiteSettingsAdmin):
    fieldsets = (
        (
            "Call To Action",
            {
                "fields": ("cta_headline", "cta_body"),
                "description": "The closing CTA strip shown near the bottom of most pages.",
            },
        ),
    )


@admin.register(ContactSettings)
class ContactSettingsAdmin(_BaseSiteSettingsAdmin):
    fieldsets = (
        (
            "Contact Info",
            {
                "fields": ("phone", "email", "address"),
                "description": "Phone, email, and physical address shown in the footer and contact page.",
            },
        ),
    )


@admin.register(SocialMediaSettings)
class SocialMediaSettingsAdmin(_BaseSiteSettingsAdmin):
    fieldsets = (
        (
            "Social Media Links",
            {
                "fields": ("facebook_url", "twitter_url", "linkedin_url", "instagram_url"),
                "description": "Social icons appear in the footer only when a URL is set.",
            },
        ),
    )
