from django.urls import path
from django.views.generic import RedirectView

from apps.leads import views

app_name = "leads"

urlpatterns = [
    path("energies/", views.coming_soon, {"vertical": "energies"}, name="energies"),
    path("farming/", views.coming_soon, {"vertical": "farming"}, name="farming"),
    path(
        "investments/",
        views.coming_soon,
        {"vertical": "investments"},
        name="investments",
    ),
    path(
        "technologies/",
        RedirectView.as_view(url="https://bjptechnologies.co.tz", permanent=True),
        name="technologies",
    ),
]
