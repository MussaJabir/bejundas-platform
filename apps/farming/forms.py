from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from apps.farming.models import OrderInquiry


class ContactForm(forms.Form):
    name = forms.CharField(max_length=200, label="Full Name")
    email = forms.EmailField(label="Email Address")
    phone = forms.CharField(max_length=30, label="Phone Number", required=False)
    subject = forms.CharField(max_length=300, label="Subject")
    message = forms.CharField(widget=forms.Textarea, label="Message")

    def send_email(self):
        data = self.cleaned_data
        phone_line = f"Phone: {data['phone']}\n" if data.get("phone") else ""
        send_mail(
            subject=f"[Bejundas Farming] {data['subject']}",
            message=(f"From: {data['name']} <{data['email']}>\n{phone_line}\n{data['message']}"),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )


# ── Phone validator shared by lead forms ─────────────────────────────


def _validate_phone(value: str) -> str:
    cleaned = (value or "").strip()
    digits = "".join(ch for ch in cleaned if ch.isdigit())
    if len(digits) < 9:
        raise ValidationError("Enter a valid phone number (minimum 9 digits).")
    return cleaned


# ── Order Inquiry form ───────────────────────────────────────────────


class OrderInquiryForm(forms.ModelForm):
    """Public order-inquiry funnel covering wholesale, retail, and
    partnership leads. Saves an OrderInquiry row and sends a branded
    notification to LEADS_EMAIL."""

    PRODUCTS_MIN_LENGTH = 3  # at least name a product

    class Meta:
        model = OrderInquiry
        fields = [
            "full_name",
            "organisation",
            "email",
            "phone",
            "inquiry_type",
            "products_of_interest",
            "quantity",
            "frequency",
            "delivery_location",
            "preferred_contact",
            "notes",
        ]
        widgets = {
            "products_of_interest": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_phone(self):
        return _validate_phone(self.cleaned_data.get("phone", ""))

    def clean_products_of_interest(self):
        value = (self.cleaned_data.get("products_of_interest") or "").strip()
        if len(value) < self.PRODUCTS_MIN_LENGTH:
            raise ValidationError(
                "Tell us at least one product you're interested in (e.g. 'eggs', "
                "'broilers', 'maize')."
            )
        return value

    def send_notification(self, request=None):
        """Plain-text + branded HTML email to LEADS_EMAIL."""
        inquiry = self.instance
        context = {
            "inquiry": inquiry,
            "site_url": request.build_absolute_uri("/") if request else "",
        }
        text_body = render_to_string("emails/order_inquiry_notification.txt", context)
        html_body = render_to_string("emails/order_inquiry_notification.html", context)
        subject = (
            f"[Bejundas Farming Order] {inquiry.organisation or inquiry.full_name} — "
            f"{inquiry.get_inquiry_type_display()}"
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.LEADS_EMAIL],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
