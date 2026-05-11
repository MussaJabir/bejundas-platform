from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("deploy/", include("apps.core.urls_webhook")),
    path("", include("apps.hub.urls")),
]
