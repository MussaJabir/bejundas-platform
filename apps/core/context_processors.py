from apps.core.models import SiteSettings


def company_info(request):
    from apps.hub.models import Service

    return {
        "company": SiteSettings.get(),
        "footer_services": Service.objects.filter(is_active=True).order_by("order")[:6],
    }


def app_theme(request):
    vertical = ""
    if getattr(request, "resolver_match", None):
        vertical = request.resolver_match.kwargs.get("vertical", "") or ""
        if not vertical:
            vertical = request.resolver_match.app_name or ""

    theme_map = {
        "financial": {"primary": "#0a2342", "accent": "#c9a84c", "label": "Financial Services"},
        "construction": {
            "primary": "#2c2c2c",
            "accent": "#f47920",
            "label": "Construction",
        },
        "energies": {"primary": "#0d3b2e", "accent": "#f9c41a", "label": "Energies"},
        "farming": {"primary": "#2d5a27", "accent": "#8bc34a", "label": "Farming"},
        "investments": {
            "primary": "#1a0533",
            "accent": "#d4af37",
            "label": "Investments",
        },
    }

    return {
        "app_theme": theme_map.get(
            vertical,
            {"primary": "#1a1a2e", "accent": "#e94560", "label": "Bejundas Group"},
        )
    }
