from django.urls import path

from apps.financial import views

app_name = "financial"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("services/", views.ServicesView.as_view(), name="services"),
    path("investments/", views.InvestmentsListView.as_view(), name="investments"),
    path(
        "investments/<slug:slug>/",
        views.InvestmentDetailView.as_view(),
        name="investment_detail",
    ),
    path("contact/", views.ContactView.as_view(), name="contact"),
]
