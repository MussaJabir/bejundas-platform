from django.conf import settings
from django.urls import include, path

from apps.leads import views

app_name = "leads"

urlpatterns = [
    path("", views.coming_soon, name="coming_soon"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
