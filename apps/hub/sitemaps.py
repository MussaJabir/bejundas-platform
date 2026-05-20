from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.hub.models import News

STATIC_PAGES = [
    ("hub:home", 1.0, "weekly"),
    ("hub:about", 0.8, "monthly"),
    ("hub:services", 0.9, "monthly"),
    ("hub:news", 0.7, "weekly"),
    ("hub:team", 0.6, "monthly"),
    ("hub:contact", 0.8, "monthly"),
    ("financial:home", 0.8, "weekly"),
    ("leads:energies", 0.7, "monthly"),
    ("leads:farming", 0.7, "monthly"),
    ("leads:investments", 0.7, "monthly"),
]


class HubStaticSitemap(Sitemap):
    def items(self):
        return STATIC_PAGES

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]


class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return News.objects.filter(published=True).order_by("-published_at")

    def lastmod(self, obj):
        return obj.published_at

    def location(self, obj):
        return reverse("hub:news_detail", kwargs={"slug": obj.slug})
