from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from apps.leads.forms import LeadForm
from apps.leads.models import VerticalPlaceholder


def coming_soon(request, vertical: str):
    placeholder = VerticalPlaceholder.objects.filter(vertical=vertical, is_active=True).first()

    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.vertical = vertical
            lead.save()
            _notify_lead(lead)
            return render(
                request,
                "leads/coming_soon.html",
                {"form": LeadForm(), "placeholder": placeholder, "submitted": True},
            )
    else:
        form = LeadForm()

    return render(
        request,
        "leads/coming_soon.html",
        {"form": form, "placeholder": placeholder},
    )


def _notify_lead(lead):
    send_mail(
        subject=f"[Bejundas Lead] {lead.vertical.title()} — {lead.name}",
        message=f"New lead from {lead.vertical}:\n\nName: {lead.name}\nEmail: {lead.email}\nPhone: {lead.phone}\n\n{lead.message}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.LEADS_EMAIL],
        fail_silently=True,
    )
