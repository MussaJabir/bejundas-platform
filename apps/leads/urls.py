from django.urls import path

from apps.leads import views

app_name = "leads"

urlpatterns = [
    path("", views.coming_soon, name="coming_soon"),
]
