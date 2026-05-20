from decimal import Decimal

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from apps.financial.models import InvestmentInquiry, LoanInquiry


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
            subject=f"[Bejundas Financial] {data['subject']}",
            message=(f"From: {data['name']} <{data['email']}>\n{phone_line}\n{data['message']}"),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )


# ── Phone validator shared by both inquiry forms ────────────────────


def _validate_phone(value: str) -> str:
    cleaned = (value or "").strip()
    digits = "".join(ch for ch in cleaned if ch.isdigit())
    if len(digits) < 9:
        raise ValidationError("Enter a valid phone number (minimum 9 digits).")
    return cleaned


# ── Loan Inquiry form ───────────────────────────────────────────────


class LoanInquiryForm(forms.ModelForm):
    """Public loan application form. 8 fields, server-side validation,
    branded HTML email notification to LEADS_EMAIL on submit."""

    NOTES_MIN_LENGTH = 0  # notes are optional — kept here as a knob

    class Meta:
        model = LoanInquiry
        fields = [
            "full_name",
            "business_name",
            "email",
            "phone",
            "loan_purpose",
            "amount_requested",
            "tenure_band",
            "preferred_contact",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_phone(self):
        return _validate_phone(self.cleaned_data.get("phone", ""))

    def clean_amount_requested(self):
        amount = self.cleaned_data.get("amount_requested")
        if amount is None or amount <= Decimal("0"):
            raise ValidationError("Amount requested must be greater than zero.")
        return amount

    def send_notification(self, request=None):
        loan = self.instance
        context = {
            "loan": loan,
            "site_url": request.build_absolute_uri("/") if request else "",
        }
        text_body = render_to_string("emails/loan_inquiry_notification.txt", context)
        html_body = render_to_string("emails/loan_inquiry_notification.html", context)
        who = loan.business_name or loan.full_name
        subject = f"[Bejundas Financial — Loan Inquiry] {who} — {loan.get_loan_purpose_display()}"
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.LEADS_EMAIL],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)


# ── Investment Inquiry form ─────────────────────────────────────────


class InvestmentInquiryForm(forms.ModelForm):
    """Public investment inquiry form. Optional offering FK is set
    server-side from the ?offering=<slug> query string in the view."""

    class Meta:
        model = InvestmentInquiry
        fields = [
            "full_name",
            "email",
            "phone",
            "capital_band",
            "preferred_tenure",
            "funding_source",
            "preferred_contact",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_phone(self):
        return _validate_phone(self.cleaned_data.get("phone", ""))

    def send_notification(self, request=None):
        inquiry = self.instance
        context = {
            "inquiry": inquiry,
            "site_url": request.build_absolute_uri("/") if request else "",
        }
        text_body = render_to_string("emails/investment_inquiry_notification.txt", context)
        html_body = render_to_string("emails/investment_inquiry_notification.html", context)
        subject = (
            f"[Bejundas Financial — Investment Inquiry] {inquiry.full_name} — "
            f"{inquiry.get_preferred_tenure_display()}"
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.LEADS_EMAIL],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
