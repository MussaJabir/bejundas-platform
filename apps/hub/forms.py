from django import forms
from django.conf import settings
from django.core.mail import send_mail


class ContactForm(forms.Form):
    name = forms.CharField(max_length=200, label="Full Name")
    email = forms.EmailField(label="Email Address")
    subject = forms.CharField(max_length=300, label="Subject")
    message = forms.CharField(widget=forms.Textarea, label="Message")

    def send_email(self):
        data = self.cleaned_data
        send_mail(
            subject=f"[Bejundas Contact] {data['subject']}",
            message=f"From: {data['name']} <{data['email']}>\n\n{data['message']}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )
