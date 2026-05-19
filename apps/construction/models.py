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


# ── Quote / RFP Request ─────────────────────────────────────────────


BUDGET_CHOICES = [
    ("under_50m", "Under 50M TZS"),
    ("50m_200m", "50M – 200M TZS"),
    ("200m_1b", "200M – 1B TZS"),
    ("over_1b", "Over 1B TZS"),
]

TIMELINE_CHOICES = [
    ("1_3", "1 – 3 months"),
    ("3_6", "3 – 6 months"),
    ("6_12", "6 – 12 months"),
    ("over_12", "12+ months"),
]

QUOTE_STATUS_CHOICES = [
    ("new", "New"),
    ("reviewed", "Reviewed"),
    ("quoted", "Quoted"),
    ("won", "Won"),
    ("lost", "Lost"),
    ("closed", "Closed"),
]


class QuoteRequest(BaseModel):
    # Contact
    full_name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True, default="")
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    # Project basics
    project_type = models.CharField(
        max_length=20,
        choices=SECTOR_CHOICES,
        help_text="Sector classification for the requested project.",
    )
    location_region = models.CharField(max_length=100)
    location_district = models.CharField(max_length=100, blank=True, default="")
    estimated_start = models.DateField(
        null=True,
        blank=True,
        help_text="Approximate start date the client has in mind.",
    )

    # Scope
    scope_description = models.TextField(
        help_text="Free-text scope description (minimum 50 characters).",
    )
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES)
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES)

    # Status workflow
    status = models.CharField(max_length=20, choices=QUOTE_STATUS_CHOICES, default="new")
    internal_notes = models.TextField(
        blank=True,
        default="",
        help_text="Admin-only notes — not visible to the client.",
    )

    class Meta:
        verbose_name = "Quote Request"
        verbose_name_plural = "Quote Requests"
        ordering = ["-created_at"]

    def __str__(self):
        company_or_name = self.company or self.full_name
        return (
            f"{company_or_name} — {self.get_project_type_display()} ({self.get_status_display()})"
        )


def _validate_attachment(file_obj):
    """Validate file size (≤5MB) and extension (PDF/JPG/PNG)."""
    from django.core.exceptions import ValidationError

    max_size = 5 * 1024 * 1024
    if file_obj.size > max_size:
        raise ValidationError("File must be 5MB or smaller.")
    allowed_extensions = {".pdf", ".jpg", ".jpeg", ".png"}
    name = file_obj.name.lower()
    if not any(name.endswith(ext) for ext in allowed_extensions):
        raise ValidationError("Only PDF, JPG, or PNG files are accepted.")


class QuoteAttachment(BaseModel):
    quote_request = models.ForeignKey(
        QuoteRequest,
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    file = models.FileField(
        upload_to="construction/quote_attachments/%Y/%m/",
        validators=[_validate_attachment],
    )

    class Meta:
        verbose_name = "Quote Attachment"
        verbose_name_plural = "Quote Attachments"
        ordering = ["created_at"]

    def __str__(self):
        return self.file.name.split("/")[-1] if self.file else "(empty)"
