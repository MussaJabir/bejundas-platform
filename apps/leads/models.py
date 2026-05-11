from django.db import models

from apps.core.models import BaseModel

VERTICAL_CHOICES = [
    ("financial", "Financial Services"),
    ("construction", "Construction"),
    ("energies", "Energies"),
    ("farming", "Farming"),
    ("investments", "Investments"),
]


class VerticalPlaceholder(BaseModel):
    vertical = models.CharField(max_length=50, choices=VERTICAL_CHOICES, unique=True)
    headline = models.CharField(max_length=300, blank=True, default="")
    subheadline = models.CharField(max_length=500, blank=True, default="")
    primary_color = models.CharField(max_length=7, default="#1a1a2e")
    accent_color = models.CharField(max_length=7, default="#e94560")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Vertical Placeholder"
        verbose_name_plural = "Vertical Placeholders"

    def __str__(self):
        return self.get_vertical_display()


class Lead(BaseModel):
    vertical = models.CharField(max_length=50, choices=VERTICAL_CHOICES)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True, default="")
    message = models.TextField(blank=True, default="")
    notified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.vertical})"
