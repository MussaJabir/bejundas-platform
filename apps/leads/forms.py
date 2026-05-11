from django import forms

from apps.leads.models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["name", "email", "phone", "message"]
        labels = {
            "name": "Full Name",
            "email": "Email Address",
            "phone": "Phone Number",
            "message": "What are you interested in?",
        }
