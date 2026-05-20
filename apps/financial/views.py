from django.shortcuts import get_object_or_404, render
from django.views import View

from apps.financial.forms import ContactForm, InvestmentInquiryForm, LoanInquiryForm
from apps.financial.models import (
    OFFERING_STATUS_CHOICES,
    SERVICE_CATEGORY_CHOICES,
    Certification,
    FinancialService,
    InvestmentOffering,
    Testimonial,
)


class HomeView(View):
    def get(self, request):
        context = {
            "featured_services": FinancialService.objects.filter(is_active=True)[:4],
            "featured_offerings": InvestmentOffering.objects.filter(
                is_featured=True, status__in=["upcoming", "open"]
            )[:3],
            "featured_testimonials": Testimonial.objects.filter(is_featured=True)[:3],
        }
        return render(request, "financial/home.html", context)


class AboutView(View):
    def get(self, request):
        context = {
            "certifications": Certification.objects.filter(is_active=True),
            "testimonials": Testimonial.objects.all()[:6],
        }
        return render(request, "financial/about.html", context)


class ServicesView(View):
    def get(self, request):
        category = request.GET.get("category", "").strip().lower()
        valid_categories = {code for code, _ in SERVICE_CATEGORY_CHOICES}
        active_category = category if category in valid_categories else ""
        services = FinancialService.objects.filter(is_active=True)
        if active_category:
            services = services.filter(category=active_category)
        return render(
            request,
            "financial/services.html",
            {
                "services": services,
                "category_choices": SERVICE_CATEGORY_CHOICES,
                "active_category": active_category,
            },
        )


class InvestmentsListView(View):
    def get(self, request):
        status = request.GET.get("status", "").strip().lower()
        valid_statuses = {code for code, _ in OFFERING_STATUS_CHOICES}
        active_status = status if status in valid_statuses else ""
        offerings = InvestmentOffering.objects.all()
        if active_status:
            offerings = offerings.filter(status=active_status)
        return render(
            request,
            "financial/investments.html",
            {
                "offerings": offerings,
                "status_choices": OFFERING_STATUS_CHOICES,
                "active_status": active_status,
            },
        )


class InvestmentDetailView(View):
    def get(self, request, slug):
        offering = get_object_or_404(InvestmentOffering, slug=slug)
        related = InvestmentOffering.objects.exclude(pk=offering.pk)[:3]
        return render(
            request,
            "financial/investment_detail.html",
            {"offering": offering, "related": related},
        )


class ContactView(View):
    def get(self, request):
        return render(request, "financial/contact.html", {"form": ContactForm()})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()
            return render(
                request,
                "financial/contact.html",
                {"form": ContactForm(), "sent": True},
            )
        return render(request, "financial/contact.html", {"form": form})


class LoanApplyView(View):
    def get(self, request):
        return render(
            request,
            "financial/loan_apply.html",
            {"form": LoanInquiryForm()},
        )

    def post(self, request):
        form = LoanInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            form.send_notification(request=request)
            return render(
                request,
                "financial/loan_apply.html",
                {"form": LoanInquiryForm(), "sent": True},
            )
        return render(request, "financial/loan_apply.html", {"form": form})


class InvestmentInquireView(View):
    """Optional ?offering=<slug> query string prefills the offering FK
    server-side so the prospect doesn't see the raw FK field."""

    def _resolve_offering(self, request):
        slug = (request.GET.get("offering") or request.POST.get("offering_slug") or "").strip()
        if not slug:
            return None
        return InvestmentOffering.objects.filter(slug=slug).first()

    def get(self, request):
        offering = self._resolve_offering(request)
        return render(
            request,
            "financial/investment_inquire.html",
            {"form": InvestmentInquiryForm(), "offering": offering},
        )

    def post(self, request):
        offering = self._resolve_offering(request)
        form = InvestmentInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.offering = offering
            inquiry.save()
            form.send_notification(request=request)
            return render(
                request,
                "financial/investment_inquire.html",
                {"form": InvestmentInquiryForm(), "offering": offering, "sent": True},
            )
        return render(
            request,
            "financial/investment_inquire.html",
            {"form": form, "offering": offering},
        )
