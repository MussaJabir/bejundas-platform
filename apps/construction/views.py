import logging

from django.shortcuts import get_object_or_404, render
from django.views import View

from apps.construction.forms import ContactForm, QuoteRequestForm
from apps.construction.models import (
    SECTOR_CHOICES,
    Certification,
    ConstructionService,
    Project,
    Testimonial,
)

logger = logging.getLogger(__name__)


class HomeView(View):
    def get(self, request):
        context = {
            "services": ConstructionService.objects.filter(is_active=True)[:4],
            "featured_projects": Project.objects.filter(is_featured=True)[:3],
            "featured_testimonials": Testimonial.objects.filter(is_featured=True)[:3],
        }
        return render(request, "construction/home.html", context)


class AboutView(View):
    def get(self, request):
        context = {
            "certifications": Certification.objects.filter(is_active=True),
            "testimonials": Testimonial.objects.all()[:6],
        }
        return render(request, "construction/about.html", context)


class ServicesView(View):
    def get(self, request):
        return render(
            request,
            "construction/services.html",
            {"services": ConstructionService.objects.filter(is_active=True)},
        )


class ProjectsView(View):
    def get(self, request):
        sector = request.GET.get("sector", "").strip().lower()
        projects = Project.objects.all()
        valid_sectors = {code for code, _ in SECTOR_CHOICES}
        active_sector = sector if sector in valid_sectors else ""
        if active_sector:
            projects = projects.filter(sector=active_sector)
        context = {
            "projects": projects,
            "sector_choices": SECTOR_CHOICES,
            "active_sector": active_sector,
        }
        return render(request, "construction/projects.html", context)


class ProjectDetailView(View):
    def get(self, request, slug):
        project = get_object_or_404(Project, slug=slug)
        related = Project.objects.filter(sector=project.sector).exclude(pk=project.pk)[:3]
        return render(
            request,
            "construction/project_detail.html",
            {"project": project, "related": related},
        )


class ContactView(View):
    def get(self, request):
        return render(request, "construction/contact.html", {"form": ContactForm()})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                form.send_email()
            except Exception:
                # Email is best-effort. Don't show a 500 because SMTP
                # is down — log and continue.
                logger.exception("Failed to send construction contact email")
            return render(
                request, "construction/contact.html", {"form": ContactForm(), "sent": True}
            )
        return render(request, "construction/contact.html", {"form": form})


class QuoteRequestView(View):
    def get(self, request):
        return render(request, "construction/quote_request.html", {"form": QuoteRequestForm()})

    def post(self, request):
        form = QuoteRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            try:
                form.send_notification(request=request)
            except Exception:
                # Quote row + attachments are saved; an SMTP failure
                # shouldn't show the requester a 500. Log and carry on.
                logger.exception("Failed to send construction quote notification email")
            return render(
                request,
                "construction/quote_request.html",
                {"form": QuoteRequestForm(), "sent": True},
            )
        return render(request, "construction/quote_request.html", {"form": form})
