from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path(
        "",
        RedirectView.as_view(url="https://bjptechnologies.co.tz", permanent=True),
        name="technologies_redirect",
    ),
]
