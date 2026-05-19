from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from apps.construction.models import QuoteAttachment, QuoteRequest, _validate_attachment


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
            subject=f"[Bejundas Construction] {data['subject']}",
            message=(
                f"From: {data['name']} <{data['email']}>\n" f"{phone_line}" f"\n{data['message']}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )


class QuoteRequestForm(forms.ModelForm):
    """Full RFP / Quote request form. 3 optional file attachments per submission."""

    SCOPE_MIN_LENGTH = 50

    attachment_1 = forms.FileField(required=False, label="Attachment 1 (optional)")
    attachment_2 = forms.FileField(required=False, label="Attachment 2 (optional)")
    attachment_3 = forms.FileField(required=False, label="Attachment 3 (optional)")

    class Meta:
        model = QuoteRequest
        fields = [
            "full_name",
            "company",
            "email",
            "phone",
            "project_type",
            "location_region",
            "location_district",
            "estimated_start",
            "scope_description",
            "budget_range",
            "timeline",
        ]
        widgets = {
            "estimated_start": forms.DateInput(attrs={"type": "date"}),
            "scope_description": forms.Textarea(attrs={"rows": 6}),
        }

    def clean_scope_description(self):
        value = self.cleaned_data["scope_description"].strip()
        if len(value) < self.SCOPE_MIN_LENGTH:
            raise ValidationError(
                f"Scope description must be at least {self.SCOPE_MIN_LENGTH} characters."
            )
        return value

    def _clean_attachment(self, field_name):
        f = self.cleaned_data.get(field_name)
        if f:
            _validate_attachment(f)
        return f

    def clean_attachment_1(self):
        return self._clean_attachment("attachment_1")

    def clean_attachment_2(self):
        return self._clean_attachment("attachment_2")

    def clean_attachment_3(self):
        return self._clean_attachment("attachment_3")

    def save(self, commit=True):
        quote = super().save(commit=commit)
        if commit:
            self._save_attachments(quote)
        return quote

    def _save_attachments(self, quote):
        for field_name in ("attachment_1", "attachment_2", "attachment_3"):
            f = self.cleaned_data.get(field_name)
            if f:
                QuoteAttachment.objects.create(quote_request=quote, file=f)

    def send_notification(self, request=None):
        """Send the notification email to LEADS_EMAIL. Plain-text + HTML alternative."""
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string

        quote = self.instance
        context = {
            "quote": quote,
            "site_url": request.build_absolute_uri("/") if request else "",
        }
        text_body = render_to_string("emails/quote_request_notification.txt", context)
        html_body = render_to_string("emails/quote_request_notification.html", context)
        subject = (
            f"[Bejundas Construction RFP] {quote.company or quote.full_name} — "
            f"{quote.get_project_type_display()}"
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.LEADS_EMAIL],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
