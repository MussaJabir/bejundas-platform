from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.construction.models import Project

STATIC_PAGES = [
    ("construction:home", 0.7, "monthly"),
    ("construction:about", 0.6, "monthly"),
    ("construction:services", 0.7, "monthly"),
    ("construction:projects", 0.7, "weekly"),
    ("construction:contact", 0.5, "monthly"),
]


class ConstructionStaticSitemap(Sitemap):
    def items(self):
        return STATIC_PAGES

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Project.objects.all().order_by("-year_completed")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("construction:project_detail", kwargs={"slug": obj.slug})
