import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(BaseModel):
    """Singleton model — always use SiteSettings.get(), never instantiate directly."""

    company_name = models.CharField(max_length=200, default="Bejundas Group of Companies")
    tagline = models.CharField(max_length=300, blank=True, default="")
    about_short = models.TextField(blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    address = models.TextField(blank=True, default="")

    facebook_url = models.URLField(blank=True, default="")
    twitter_url = models.URLField(blank=True, default="")
    linkedin_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")

    logo = models.ImageField(upload_to="brand/", blank=True)
    favicon = models.ImageField(upload_to="brand/", blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.company_name

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk="00000000-0000-0000-0000-000000000001")
        return obj
