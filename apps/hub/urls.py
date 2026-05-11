from django.urls import path

from apps.hub import views

app_name = "hub"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("services/", views.ServicesView.as_view(), name="services"),
    path("news/", views.NewsListView.as_view(), name="news"),
    path("news/<slug:slug>/", views.NewsDetailView.as_view(), name="news_detail"),
    path("team/", views.TeamView.as_view(), name="team"),
    path("contact/", views.ContactView.as_view(), name="contact"),
]
