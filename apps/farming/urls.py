from django.urls import path

from apps.farming import views

app_name = "farming"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]
