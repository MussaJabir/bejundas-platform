from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.core.models import BaseModel

# ── Choice catalogues ──────────────────────────────────────────────


SERVICE_CATEGORY_CHOICES = [
    ("loans", "Microfinance & Lending"),
    ("investments", "Investments & Partnerships"),
    ("agency", "Agency & Franchising"),
    ("securities", "Government Securities & DSE"),
    ("auto", "Auto & Asset Services"),
]


OFFERING_STATUS_CHOICES = [
    ("upcoming", "Upcoming"),
    ("open", "Open"),
    ("closed", "Closed"),
]


PAYOUT_CADENCE_CHOICES = [
    ("quarterly", "Quarterly (every 3 months)"),
    ("semi_annual", "Semi-annual"),
    ("annual", "Annual"),
    ("maturity", "At maturity"),
]


LOAN_PURPOSE_CHOICES = [
    ("personal", "Personal"),
    ("sme", "SME / Business"),
    ("group", "Group Loan"),
    ("asset", "Asset Finance"),
]


TENURE_BAND_CHOICES = [
    ("under_6", "Under 6 months"),
    ("6_12", "6 – 12 months"),
    ("12_24", "1 – 2 years"),
    ("over_24", "2+ years"),
]


CAPITAL_BAND_CHOICES = [
    ("250k_1m", "TZS 250,000 – 1,000,000"),
    ("1m_5m", "TZS 1,000,000 – 5,000,000"),
    ("5m_10m", "TZS 5,000,000 – 10,000,000"),
    ("over_10m", "TZS 10,000,000+"),
]


PREFERRED_CONTACT_CHOICES = [
    ("phone", "Phone Call"),
    ("whatsapp", "WhatsApp"),
    ("email", "Email"),
]


FUNDING_SOURCE_CHOICES = [
    ("savings", "Personal Savings"),
    ("business", "Business Profits"),
    ("sale", "Sale of Asset"),
    ("other", "Other"),
]


LOAN_STATUS_CHOICES = [
    ("new", "New"),
    ("reviewed", "Reviewed"),
    ("approved", "Approved"),
    ("disbursed", "Disbursed"),
    ("declined", "Declined"),
    ("closed", "Closed"),
]


INVESTMENT_STATUS_CHOICES = [
    ("new", "New"),
    ("contacted", "Contacted"),
    ("committed", "Committed"),
    ("funded", "Funded"),
    ("active", "Active"),
    ("matured", "Matured"),
    ("lost", "Lost"),
]


PREFERRED_TENURE_CHOICES = [
    ("1yr", "1 Year (BFS/IO/2026/01)"),
    ("2yr", "2 Years (BFS/IO/2026/02)"),
    ("undecided", "Undecided / Discuss"),
]


# ── Catalogue models ────────────────────────────────────────────────


class FinancialService(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(
        max_length=20,
        choices=SERVICE_CATEGORY_CHOICES,
        help_text="Groups services on the /financial/services/ page.",
    )
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
        help_text="Material Symbols icon name (e.g. 'savings', 'account_balance').",
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Financial Service"
        verbose_name_plural = "Financial Services"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class InvestmentOffering(BaseModel):
    reference_id = models.CharField(
        max_length=40,
        unique=True,
        help_text="Public reference (e.g. 'BFS/IO/2026/01').",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    tenure_months = models.PositiveIntegerField(help_text="Tenure in months (e.g. 12, 24).")
    indicative_rate_pct = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Indicative annual rate, e.g. 16.50 for 16.5%.",
    )
    min_capital = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Minimum capital in TZS.",
    )
    payout_cadence = models.CharField(
        max_length=20,
        choices=PAYOUT_CADENCE_CHOICES,
        default="quarterly",
    )
    opens_at = models.DateField(null=True, blank=True)
    closes_at = models.DateField(null=True, blank=True)
    settlement_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date the principal is returned to the investor.",
    )
    status = models.CharField(
        max_length=20,
        choices=OFFERING_STATUS_CHOICES,
        default="upcoming",
    )
    description = models.TextField(
        blank=True,
        default="",
        help_text="Narrative description shown on the offering detail page.",
    )
    payout_calendar_notes = models.TextField(
        blank=True,
        default="",
        help_text="Free-text calendar / dates table content (interest payment schedule).",
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Featured offerings appear on the homepage.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Investment Offering"
        verbose_name_plural = "Investment Offerings"
        ordering = ["order", "-opens_at"]

    def __str__(self):
        return f"{self.reference_id} — {self.title}"

    def get_absolute_url(self):
        """Powers the Unfold admin "View on site" link so the client
        can preview an offering after editing it."""
        return reverse("financial:investment_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.reference_id.replace("/", "-"))
        super().save(*args, **kwargs)


class Testimonial(BaseModel):
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
        help_text="Client company / organisation name.",
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
    name = models.CharField(
        max_length=200,
        help_text="Registration / licence name (e.g. 'BoT Agency Banking Registration').",
    )
    issuer = models.CharField(
        max_length=200,
        help_text="Issuing body (e.g. 'Bank of Tanzania', 'BRELA').",
    )
    reference_number = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Public registration / licence number, if any.",
    )
    year_awarded = models.PositiveIntegerField(null=True, blank=True)
    certificate_image = models.ImageField(
        upload_to="financial/certifications/",
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


# ── Lead models ─────────────────────────────────────────────────────


class LoanInquiry(BaseModel):
    # Contact
    full_name = models.CharField(max_length=200)
    business_name = models.CharField(max_length=200, blank=True, default="")
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    # Loan need
    loan_purpose = models.CharField(max_length=20, choices=LOAN_PURPOSE_CHOICES)
    amount_requested = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Requested amount in TZS.",
    )
    tenure_band = models.CharField(max_length=20, choices=TENURE_BAND_CHOICES)
    preferred_contact = models.CharField(
        max_length=20,
        choices=PREFERRED_CONTACT_CHOICES,
        default="phone",
    )

    notes = models.TextField(
        blank=True,
        default="",
        help_text="Free-text notes from the applicant.",
    )

    # Workflow
    status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default="new")
    internal_notes = models.TextField(
        blank=True,
        default="",
        help_text="Admin-only notes — not visible to the applicant.",
    )

    class Meta:
        verbose_name = "Loan Inquiry"
        verbose_name_plural = "Loan Inquiries"
        ordering = ["-created_at"]

    def __str__(self):
        who = self.business_name or self.full_name
        return f"{who} — {self.get_loan_purpose_display()} ({self.get_status_display()})"


class InvestmentInquiry(BaseModel):
    # Contact
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    # Investment intent
    capital_band = models.CharField(max_length=20, choices=CAPITAL_BAND_CHOICES)
    preferred_tenure = models.CharField(
        max_length=20,
        choices=PREFERRED_TENURE_CHOICES,
        default="undecided",
    )
    funding_source = models.CharField(
        max_length=20,
        choices=FUNDING_SOURCE_CHOICES,
        default="savings",
    )
    offering = models.ForeignKey(
        InvestmentOffering,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inquiries",
        help_text="Specific offering the prospect referenced (optional).",
    )
    preferred_contact = models.CharField(
        max_length=20,
        choices=PREFERRED_CONTACT_CHOICES,
        default="phone",
    )

    notes = models.TextField(
        blank=True,
        default="",
        help_text="Free-text notes from the prospect.",
    )

    # Workflow
    status = models.CharField(max_length=20, choices=INVESTMENT_STATUS_CHOICES, default="new")
    internal_notes = models.TextField(
        blank=True,
        default="",
        help_text="Admin-only notes — not visible to the prospect.",
    )

    class Meta:
        verbose_name = "Investment Inquiry"
        verbose_name_plural = "Investment Inquiries"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.full_name} — {self.get_preferred_tenure_display()} "
            f"({self.get_status_display()})"
        )
