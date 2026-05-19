from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path

from apps.hub.sitemaps import HubStaticSitemap, NewsSitemap

sitemaps = {
    "static": HubStaticSitemap,
    "news": NewsSitemap,
}


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /deploy/",
        f"Sitemap: https://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("deploy/", include("apps.core.urls_webhook")),
    path(
        "sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"
    ),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("construction/", include("apps.construction.urls")),
    path("", include("apps.leads.urls")),
    path("", include("apps.hub.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
