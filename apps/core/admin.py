from datetime import timedelta

from django.contrib import admin
from django.shortcuts import redirect
from django.utils import timezone
from unfold.admin import ModelAdmin

from apps.core.models import SiteSettings


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
