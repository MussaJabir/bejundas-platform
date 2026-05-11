from apps.core.models import SiteSettings


def company_info(request):
    return {"company": SiteSettings.get()}


def app_theme(request):
    host = request.get_host().split(":")[0]
    subdomain = host.split(".")[0] if "." in host else ""

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
            subdomain,
            {"primary": "#1a1a2e", "accent": "#e94560", "label": "Bejundas Group"},
        )
    }
