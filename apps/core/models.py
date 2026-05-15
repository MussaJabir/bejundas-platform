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

    # Hero section
    hero_headline = models.CharField(
        max_length=300, blank=True, default="Empowering Tanzania With Business Excellence"
    )
    hero_subheadline = models.CharField(
        max_length=500,
        blank=True,
        default="Building scalable, high-impact solutions to help you grow with confidence.",
    )
    hero_cta_text = models.CharField(max_length=100, blank=True, default="View Our Services")

    # About section
    about_headline = models.CharField(
        max_length=300, blank=True, default="We Turn Vision Into Reality"
    )
    about_body = models.TextField(
        blank=True,
        default="As a trusted corporate partner, we specialize in delivering strategic solutions, combining business insight and innovation to drive results.",
    )
    about_video_url = models.URLField(blank=True, default="")
    years_experience = models.PositiveIntegerField(default=10)
    projects_count = models.PositiveIntegerField(default=50)
    clients_count = models.PositiveIntegerField(default=30)
    satisfaction_pct = models.PositiveIntegerField(default=98)

    # Mission & Vision
    mission = models.TextField(
        blank=True,
        default="To empower Tanzanian businesses through diversified, innovative, and sustainable solutions.",
    )
    vision = models.TextField(
        blank=True, default="To be Tanzania's most trusted and impactful group of companies."
    )

    # CTA section
    cta_headline = models.CharField(
        max_length=300, blank=True, default="Ready To Take Your Business Further?"
    )
    cta_body = models.CharField(
        max_length=500,
        blank=True,
        default="Let's discuss how we can help you achieve your business goals.",
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.company_name

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk="00000000-0000-0000-0000-000000000001")
        return obj


# --- Proxy admin sections ---
# Each proxy is the same SiteSettings row, displayed via a focused admin
# fieldset so the sidebar splits one giant form into seven discrete entries.


class IdentitySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Identity & Branding"
        verbose_name_plural = "Identity & Branding"


class HeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"


class AboutSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "About Section"
        verbose_name_plural = "About Section"


class MissionVisionSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Mission & Vision"
        verbose_name_plural = "Mission & Vision"


class CTASettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "CTA Section"
        verbose_name_plural = "CTA Section"


class ContactSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"


class SocialMediaSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Social Media"
        verbose_name_plural = "Social Media"
