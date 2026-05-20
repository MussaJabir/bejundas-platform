from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.financial.models import InvestmentOffering

STATIC_PAGES = [
    ("financial:home", 0.9, "weekly"),
    ("financial:about", 0.7, "monthly"),
    ("financial:services", 0.8, "monthly"),
    ("financial:investments", 0.8, "weekly"),
    ("financial:contact", 0.7, "monthly"),
    ("financial:loan_apply", 0.8, "monthly"),
    ("financial:invest_inquire", 0.8, "monthly"),
]


class FinancialStaticSitemap(Sitemap):
    def items(self):
        return STATIC_PAGES

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]


class InvestmentOfferingSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return InvestmentOffering.objects.all().order_by("-opens_at")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("financial:investment_detail", kwargs={"slug": obj.slug})
