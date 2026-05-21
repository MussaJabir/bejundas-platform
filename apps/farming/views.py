import logging

from django.shortcuts import render
from django.views import View

from apps.farming.forms import ContactForm
from apps.farming.models import (
    PRODUCT_CATEGORY_CHOICES,
    Certification,
    Farm,
    FarmingProduct,
    Testimonial,
)

logger = logging.getLogger(__name__)


class HomeView(View):
    def get(self, request):
        context = {
            "featured_products": FarmingProduct.objects.filter(is_active=True, is_featured=True)[
                :6
            ],
            "featured_farms": Farm.objects.all()[:2],
            "featured_testimonials": Testimonial.objects.filter(is_featured=True)[:3],
        }
        return render(request, "farming/home.html", context)


class AboutView(View):
    def get(self, request):
        context = {
            "certifications": Certification.objects.filter(is_active=True),
            "testimonials": Testimonial.objects.all()[:6],
        }
        return render(request, "farming/about.html", context)


class ProductsView(View):
    def get(self, request):
        category = request.GET.get("category", "").strip().lower()
        products = FarmingProduct.objects.filter(is_active=True)
        valid = {code for code, _ in PRODUCT_CATEGORY_CHOICES}
        active_category = category if category in valid else ""
        if active_category:
            products = products.filter(category=active_category)
        context = {
            "products": products,
            "category_choices": PRODUCT_CATEGORY_CHOICES,
            "active_category": active_category,
        }
        return render(request, "farming/products.html", context)


class FarmsView(View):
    def get(self, request):
        return render(request, "farming/farms.html", {"farms": Farm.objects.all()})


class ContactView(View):
    def get(self, request):
        return render(request, "farming/contact.html", {"form": ContactForm()})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                form.send_email()
            except Exception:
                # Best-effort — don't 500 the visitor because SMTP is down.
                logger.exception("Failed to send farming contact email")
            return render(request, "farming/contact.html", {"form": ContactForm(), "sent": True})
        return render(request, "farming/contact.html", {"form": form})
