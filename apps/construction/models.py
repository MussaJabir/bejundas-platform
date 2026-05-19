from django.db import models
from django.utils.text import slugify

from apps.core.models import BaseModel

SECTOR_CHOICES = [
    ("residential", "Residential"),
    ("commercial", "Commercial"),
    ("civil", "Civil Works"),
    ("industrial", "Industrial"),
    ("fitout", "Interior Fit-out"),
    ("renovation", "Renovation"),
]


class ConstructionService(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.CharField(
        max_length=300,
        help_text="One-line pitch shown on service cards.",
    )
    description = models.TextField(
        blank=True,
        default="",
        help_text="Full description for the service detail section.",
    )
    icon = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Material Symbols icon name (e.g. 'engineering', 'apartment').",
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Construction Service"
        verbose_name_plural = "Construction Services"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(BaseModel):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES)
    location_city = models.CharField(max_length=100)
    location_region = models.CharField(max_length=100, blank=True, default="")
    year_completed = models.PositiveIntegerField()
    description = models.TextField(
        blank=True,
        default="",
        help_text="Project narrative shown on the detail page.",
    )
    cover_image = models.ImageField(
        upload_to="construction/projects/",
        blank=True,
        help_text="Hero image for the project card and detail page. 16:9 looks best.",
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Featured projects appear in the homepage 'Featured Projects' strip.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["order", "-year_completed", "title"]

    def __str__(self):
        return f"{self.title} ({self.year_completed})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Testimonial(BaseModel):
    # Opt out of pytest collection — the "Test*" prefix triggers pytest's
    # default python_classes pattern, producing a noisy warning otherwise.
    __test__ = False

    author_name = models.CharField(max_length=200)
    author_role = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="e.g. 'Managing Director'",
    )
    organisation = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Client company / institution name.",
    )
    quote = models.TextField(help_text="The client's testimonial text.")
    is_featured = models.BooleanField(
        default=False,
        help_text="Featured testimonials surface on the homepage.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return (
            f"{self.author_name} — {self.organisation}" if self.organisation else self.author_name
        )


class Certification(BaseModel):
    name = models.CharField(max_length=200)
    issuer = models.CharField(
        max_length=200,
        help_text="Issuing body (e.g. 'NCC Tanzania', 'ISO').",
    )
    year_awarded = models.PositiveIntegerField()
    certificate_image = models.ImageField(
        upload_to="construction/certifications/",
        blank=True,
        help_text="Optional scan / logo of the certificate.",
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"
        ordering = ["order", "-year_awarded"]

    def __str__(self):
        return f"{self.name} ({self.issuer})"
