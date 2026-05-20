from django.urls import path

from apps.financial import views

app_name = "financial"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]
