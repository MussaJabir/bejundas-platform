from django.db import models
from django.utils.text import slugify

from apps.core.models import BaseModel

# ── Choice catalogues ──────────────────────────────────────────────


PRODUCT_CATEGORY_CHOICES = [
    ("crops", "Crops"),
    ("poultry", "Poultry"),
    ("processed", "Processed Goods"),
]


UNIT_CHOICES = [
    ("kg", "Kilogram (kg)"),
    ("dozen", "Dozen (eg. eggs)"),
    ("each", "Each (per bird)"),
    ("litre", "Litre"),
    ("bag", "Bag (50 kg)"),
]


INQUIRY_TYPE_CHOICES = [
    ("wholesale", "Wholesale Buyer"),
    ("retail", "Retail Customer"),
    ("partnership", "Partnership / Contract Farming"),
]


FREQUENCY_CHOICES = [
    ("one_off", "One-off Order"),
    ("monthly", "Monthly / Recurring"),
    ("seasonal", "Seasonal"),
]


PREFERRED_CONTACT_CHOICES = [
    ("phone", "Phone Call"),
    ("whatsapp", "WhatsApp"),
    ("email", "Email"),
]


# 6-state OrderInquiry workflow per the Phase 1 plan.
INQUIRY_STATUS_CHOICES = [
    ("new", "New"),
    ("contacted", "Contacted"),
    ("quoted", "Quoted"),
    ("fulfilled", "Fulfilled"),
    ("declined", "Declined"),
    ("closed", "Closed"),
]


# ── Catalogue models ────────────────────────────────────────────────


class FarmingProduct(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(
        max_length=20,
        choices=PRODUCT_CATEGORY_CHOICES,
        help_text="Groups products on the /farming/products/ page.",
    )
    summary = models.CharField(
        max_length=300,
        help_text="One-line pitch shown on product cards.",
    )
    description = models.TextField(
        blank=True,
        default="",
        help_text="Full description for the product detail section.",
    )
    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default="kg",
        help_text="Default selling unit — inform buyers without quoting a price.",
    )
    image = models.ImageField(
        upload_to="farming/products/",
        blank=True,
        help_text="Optional product photo. Square crop reads best on cards.",
    )
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(
        default=False,
        help_text="Featured products appear on the homepage strip.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Farming Product"
        verbose_name_plural = "Farming Products"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Farm(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    region = models.CharField(
        max_length=100,
        help_text="Tanzanian region the farm sits in (e.g. 'Mbeya', 'Pwani').",
    )
    size_hectares = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Approximate land size in hectares (leave blank if not disclosed).",
    )
    primary_activity = models.CharField(
        max_length=20,
        choices=PRODUCT_CATEGORY_CHOICES,
        help_text="What this farm mainly produces.",
    )
    description = models.TextField(
        blank=True,
        default="",
        help_text="Narrative shown on the /farming/farms/ page card.",
    )
    cover_image = models.ImageField(
        upload_to="farming/farms/",
        blank=True,
        help_text="Cover photo for the farm card. 16:9 looks best.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Farm"
        verbose_name_plural = "Farms"
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} ({self.region})"

    def get_absolute_url(self):
        """Powers Unfold's admin 'View on site' button. The farms list URL
        ships in Phase 3 — until then this anchor URL is harmless (it just
        404s rather than crashes admin)."""
        return f"/farming/farms/#{self.slug}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
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
        help_text="e.g. 'Procurement Manager'",
    )
    organisation = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Buyer / partner / cooperative name.",
    )
    quote = models.TextField(help_text="The customer's testimonial text.")
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
    name = models.CharField(
        max_length=200,
        help_text="Registration / licence name (e.g. 'TBS Food Safety Mark').",
    )
    issuer = models.CharField(
        max_length=200,
        help_text="Issuing body (e.g. 'Tanzania Bureau of Standards').",
    )
    reference_number = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Public registration / licence number, if any.",
    )
    year_awarded = models.PositiveIntegerField(null=True, blank=True)
    certificate_image = models.ImageField(
        upload_to="farming/certifications/",
        blank=True,
        help_text="Optional scan / logo of the certificate.",
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Certification / Registration"
        verbose_name_plural = "Certifications / Registrations"
        ordering = ["order", "-year_awarded"]

    def __str__(self):
        return f"{self.name} ({self.issuer})"


# ── Lead model ──────────────────────────────────────────────────────


class OrderInquiry(BaseModel):
    # Contact
    full_name = models.CharField(max_length=200)
    organisation = models.CharField(max_length=200, blank=True, default="")
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    # Order intent
    inquiry_type = models.CharField(
        max_length=20,
        choices=INQUIRY_TYPE_CHOICES,
        default="wholesale",
    )
    products_of_interest = models.TextField(
        help_text="Free-text list of products the buyer wants (kept simple — "
        "not M2M so partial / mistyped names still capture the lead).",
    )
    quantity = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Approximate quantity / volume (e.g. '500 kg', '20 trays', "
        "'2 tonnes / month'). Free-text — units vary by product.",
    )
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default="one_off",
    )
    delivery_location = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Region / city where the buyer wants delivery (optional).",
    )
    preferred_contact = models.CharField(
        max_length=20,
        choices=PREFERRED_CONTACT_CHOICES,
        default="phone",
    )

    notes = models.TextField(
        blank=True,
        default="",
        help_text="Free-text notes from the buyer.",
    )

    # Workflow
    status = models.CharField(max_length=20, choices=INQUIRY_STATUS_CHOICES, default="new")
    internal_notes = models.TextField(
        blank=True,
        default="",
        help_text="Admin-only notes — not visible to the buyer.",
    )

    class Meta:
        verbose_name = "Order Inquiry"
        verbose_name_plural = "Order Inquiries"
        ordering = ["-created_at"]

    def __str__(self):
        who = self.organisation or self.full_name
        return f"{who} — {self.get_inquiry_type_display()} ({self.get_status_display()})"
