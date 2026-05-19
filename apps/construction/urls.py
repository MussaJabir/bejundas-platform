from django.urls import path

from apps.construction import views

app_name = "construction"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]
