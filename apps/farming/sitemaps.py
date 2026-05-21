from django.contrib.sitemaps import Sitemap
from django.urls import reverse

STATIC_PAGES = [
    ("farming:home", 0.9, "weekly"),
]


class FarmingStaticSitemap(Sitemap):
    def items(self):
        return STATIC_PAGES

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]
