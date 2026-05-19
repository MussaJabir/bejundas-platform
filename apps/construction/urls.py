from django.urls import path

from apps.construction import views

app_name = "construction"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("services/", views.ServicesView.as_view(), name="services"),
    path("projects/", views.ProjectsView.as_view(), name="projects"),
    path("projects/<slug:slug>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("quote/", views.QuoteRequestView.as_view(), name="quote_request"),
]
