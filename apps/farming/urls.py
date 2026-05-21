from django.urls import path

from apps.farming import views

app_name = "farming"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("products/", views.ProductsView.as_view(), name="products"),
    path("farms/", views.FarmsView.as_view(), name="farms"),
    path("order/", views.OrderInquireView.as_view(), name="order"),
    path("contact/", views.ContactView.as_view(), name="contact"),
]
