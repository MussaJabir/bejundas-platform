from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from apps.financial.models import (
    Certification,
    FinancialService,
    InvestmentInquiry,
    InvestmentOffering,
    LoanInquiry,
    Testimonial,
)

# ── Shared pill helpers ─────────────────────────────────────────────


def _pill(text: str, bg: str, fg: str) -> str:
    return (
        f'<span style="background:{bg};color:{fg};font-size:11px;font-weight:700;'
        f"padding:2px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em;"
        f'">{text}</span>'
    )


def _status_pill(is_active: bool) -> str:
    return (
        _pill("Active", "#dcfce7", "#166534")
        if is_active
        else _pill("Inactive", "#f1f5f9", "#64748b")
    )


def _featured_pill(is_featured: bool) -> str:
    return (
        _pill("Featured", "#fdf8e9", "#a98a35")
        if is_featured
        else _pill("Standard", "#f1f5f9", "#64748b")
    )


# ── Colour maps (navy / gold spectrum) ──────────────────────────────


_CATEGORY_COLOURS = {
    "loans": ("#dbeafe", "#1d4ed8"),
    "investments": ("#fdf8e9", "#a98a35"),
    "agency": ("#dcfce7", "#166534"),
    "securities": ("#e0e7ff", "#4338ca"),
    "auto": ("#fee2e2", "#b91c1c"),
    "insurance": ("#cffafe", "#0e7490"),
}


_OFFERING_STATUS_COLOURS = {
    "upcoming": ("#dbeafe", "#1d4ed8"),
    "open": ("#dcfce7", "#166534"),
    "closed": ("#f1f5f9", "#64748b"),
}


_LOAN_STATUS_COLOURS = {
    "new": ("#fee2e2", "#991b1b"),
    "reviewed": ("#dbeafe", "#1d4ed8"),
    "approved": ("#fef3c7", "#a16207"),
    "disbursed": ("#dcfce7", "#166534"),
    "declined": ("#f1f5f9", "#64748b"),
    "closed": ("#e2e8f0", "#475569"),
}


_INVESTMENT_STATUS_COLOURS = {
    "new": ("#fee2e2", "#991b1b"),
    "contacted": ("#dbeafe", "#1d4ed8"),
    "committed": ("#fef3c7", "#a16207"),
    "funded": ("#fdf8e9", "#a98a35"),
    "active": ("#dcfce7", "#166534"),
    "matured": ("#e2e8f0", "#475569"),
    "lost": ("#f1f5f9", "#64748b"),
}


# ── Catalogue admins ────────────────────────────────────────────────


@admin.register(FinancialService)
class FinancialServiceAdmin(ModelAdmin):
    list_display = ["name", "category_pill", "icon_chip", "order", "status_pill"]
    list_filter = ["category", "is_active"]
    search_fields = ["name", "summary", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 20
    ordering = ["order", "name"]
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "slug", "category", "summary", "description", "icon"),
                "description": (
                    "Financial services shown on the /financial/services/ page, "
                    "grouped by category."
                ),
            },
        ),
        (
            "Display",
            {
                "fields": ("order", "is_active"),
                "description": "Lower 'order' values appear first.",
            },
        ),
    )

    @admin.display(description="Category", ordering="category")
    def category_pill(self, obj):
        bg, fg = _CATEGORY_COLOURS.get(obj.category, ("#f1f5f9", "#64748b"))
        return format_html(_pill(obj.get_category_display(), bg, fg))

    @admin.display(description="Icon", ordering="icon")
    def icon_chip(self, obj):
        if not obj.icon:
            return "—"
        return format_html(
            '<code style="font-family:monospace;font-size:11px;background:#fdf8e9;color:#a98a35;'
            'padding:2px 8px;border-radius:4px;">{}</code>',
            obj.icon,
        )

    @admin.display(description="Status", ordering="is_active")
    def status_pill(self, obj):
        return format_html(_status_pill(obj.is_active))


@admin.register(InvestmentOffering)
class InvestmentOfferingAdmin(ModelAdmin):
    list_display = [
        "reference_id",
        "title",
        "tenure_label",
        "rate_label",
        "min_capital_label",
        "status_pill",
        "featured_pill",
    ]
    list_display_links = ["reference_id", "title"]
    list_filter = ["status", "tenure_months", "is_featured"]
    search_fields = ["reference_id", "title", "description"]
    prepopulated_fields = {"slug": ("reference_id",)}
    list_per_page = 25
    ordering = ["order", "-opens_at"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "reference_id",
                    "title",
                    "slug",
                    "description",
                ),
                "description": ("Productised investment rounds (e.g. BFS/IO/2026/01)."),
            },
        ),
        (
            "Terms",
            {
                "fields": (
                    "tenure_months",
                    "indicative_rate_pct",
                    "min_capital",
                    "payout_cadence",
                ),
            },
        ),
        (
            "Calendar",
            {
                "fields": (
                    "opens_at",
                    "closes_at",
                    "settlement_date",
                    "payout_calendar_notes",
                ),
            },
        ),
        (
            "Display",
            {
                "fields": ("status", "is_featured", "order"),
            },
        ),
    )

    @admin.display(description="Tenure", ordering="tenure_months")
    def tenure_label(self, obj):
        years = obj.tenure_months // 12
        rest = obj.tenure_months % 12
        if years and not rest:
            return f"{years}y"
        if not years:
            return f"{rest}m"
        return f"{years}y {rest}m"

    @admin.display(description="Rate", ordering="indicative_rate_pct")
    def rate_label(self, obj):
        return f"{obj.indicative_rate_pct:.2f}% p.a."

    @admin.display(description="Min Capital", ordering="min_capital")
    def min_capital_label(self, obj):
        return f"TZS {obj.min_capital:,.0f}"

    @admin.display(description="Status", ordering="status")
    def status_pill(self, obj):
        bg, fg = _OFFERING_STATUS_COLOURS.get(obj.status, ("#f1f5f9", "#64748b"))
        return format_html(_pill(obj.get_status_display(), bg, fg))

    @admin.display(description="Featured", ordering="is_featured")
    def featured_pill(self, obj):
        return format_html(_featured_pill(obj.is_featured))


@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ["author_name", "author_role", "organisation", "order", "featured_pill"]
    list_filter = ["is_featured"]
    search_fields = ["author_name", "organisation", "quote"]
    list_per_page = 25
    ordering = ["order", "-created_at"]
    fieldsets = (
        (
            None,
            {
                "fields": ("author_name", "author_role", "organisation", "quote"),
                "description": "Client testimonials. Featured ones surface on the homepage.",
            },
        ),
        ("Display", {"fields": ("is_featured", "order")}),
    )

    @admin.display(description="Featured", ordering="is_featured")
    def featured_pill(self, obj):
        return format_html(_featured_pill(obj.is_featured))


@admin.register(Certification)
class CertificationAdmin(ModelAdmin):
    list_display = [
        "certificate_thumbnail",
        "name",
        "issuer",
        "reference_number",
        "year_awarded",
        "order",
        "status_pill",
    ]
    list_display_links = ["certificate_thumbnail", "name"]
    list_filter = ["is_active", "year_awarded"]
    search_fields = ["name", "issuer", "reference_number"]
    list_per_page = 25
    ordering = ["order", "-year_awarded"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "issuer",
                    "reference_number",
                    "year_awarded",
                    "certificate_image",
                ),
                "description": "Registrations / licences shown on the About page.",
            },
        ),
        ("Display", {"fields": ("is_active", "order")}),
    )

    @admin.display(description="Image")
    def certificate_thumbnail(self, obj):
        if obj.certificate_image:
            return format_html(
                '<img src="{}" style="width:48px;height:48px;border-radius:6px;object-fit:contain;'
                'background:#fff;border:1px solid #e2e8f0;padding:2px;" alt="">',
                obj.certificate_image.url,
            )
        return format_html(
            '<span style="display:inline-flex;width:48px;height:48px;border-radius:6px;'
            "background:#f1f5f9;color:#94a3b8;align-items:center;justify-content:center;"
            'font-size:18px;border:1px solid #e2e8f0;">&#10003;</span>'
        )

    @admin.display(description="Status", ordering="is_active")
    def status_pill(self, obj):
        return format_html(_status_pill(obj.is_active))


# ── Lead admins ─────────────────────────────────────────────────────


@admin.register(LoanInquiry)
class LoanInquiryAdmin(ModelAdmin):
    list_display = [
        "submitted_label",
        "who",
        "purpose_label",
        "amount_label",
        "tenure_band",
        "status_pill",
    ]
    list_filter = ["status", "loan_purpose", "tenure_band", "created_at"]
    search_fields = ["full_name", "business_name", "email", "phone", "notes"]
    readonly_fields = [
        "full_name",
        "business_name",
        "email",
        "phone",
        "loan_purpose",
        "amount_requested",
        "tenure_band",
        "preferred_contact",
        "notes",
        "created_at",
    ]
    list_per_page = 25
    actions = [
        "mark_as_reviewed",
        "mark_as_approved",
        "mark_as_disbursed",
        "mark_as_declined",
        "mark_as_closed",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": ("status", "internal_notes"),
                "description": (
                    "Workflow: New → Reviewed → Approved → Disbursed (or Declined / Closed)."
                ),
            },
        ),
        (
            "Applicant",
            {
                "fields": ("full_name", "business_name", "email", "phone", "preferred_contact"),
                "description": "Submitted contact details (read-only).",
            },
        ),
        (
            "Loan Need",
            {
                "fields": ("loan_purpose", "amount_requested", "tenure_band", "notes"),
            },
        ),
        ("Meta", {"fields": ("created_at",)}),
    )

    @admin.display(description="Submitted", ordering="-created_at")
    def submitted_label(self, obj):
        return obj.created_at.strftime("%d %b %Y")

    @admin.display(description="Applicant")
    def who(self, obj):
        return obj.business_name or obj.full_name

    @admin.display(description="Purpose", ordering="loan_purpose")
    def purpose_label(self, obj):
        return obj.get_loan_purpose_display()

    @admin.display(description="Amount", ordering="amount_requested")
    def amount_label(self, obj):
        return f"TZS {obj.amount_requested:,.0f}"

    @admin.display(description="Status", ordering="status")
    def status_pill(self, obj):
        bg, fg = _LOAN_STATUS_COLOURS.get(obj.status, ("#f1f5f9", "#64748b"))
        return format_html(_pill(obj.get_status_display(), bg, fg))

    def _bulk_set_status(self, request, queryset, new_status, label):
        updated = queryset.update(status=new_status)
        self.message_user(
            request,
            f"{updated} loan inquir{'ies' if updated != 1 else 'y'} marked as {label}.",
        )

    @admin.action(description="Mark selected as Reviewed")
    def mark_as_reviewed(self, request, queryset):
        self._bulk_set_status(request, queryset, "reviewed", "reviewed")

    @admin.action(description="Mark selected as Approved")
    def mark_as_approved(self, request, queryset):
        self._bulk_set_status(request, queryset, "approved", "approved")

    @admin.action(description="Mark selected as Disbursed")
    def mark_as_disbursed(self, request, queryset):
        self._bulk_set_status(request, queryset, "disbursed", "disbursed")

    @admin.action(description="Mark selected as Declined")
    def mark_as_declined(self, request, queryset):
        self._bulk_set_status(request, queryset, "declined", "declined")

    @admin.action(description="Mark selected as Closed")
    def mark_as_closed(self, request, queryset):
        self._bulk_set_status(request, queryset, "closed", "closed")


@admin.register(InvestmentInquiry)
class InvestmentInquiryAdmin(ModelAdmin):
    list_display = [
        "submitted_label",
        "full_name",
        "capital_label",
        "tenure_label",
        "offering_label",
        "status_pill",
    ]
    list_filter = ["status", "preferred_tenure", "capital_band", "created_at"]
    search_fields = ["full_name", "email", "phone", "notes"]
    autocomplete_fields = ["offering"]
    readonly_fields = [
        "full_name",
        "email",
        "phone",
        "capital_band",
        "preferred_tenure",
        "funding_source",
        "offering",
        "preferred_contact",
        "notes",
        "created_at",
    ]
    list_per_page = 25
    actions = [
        "mark_as_contacted",
        "mark_as_committed",
        "mark_as_funded",
        "mark_as_active",
        "mark_as_matured",
        "mark_as_lost",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": ("status", "internal_notes"),
                "description": (
                    "Workflow: New → Contacted → Committed → Funded → Active → "
                    "Matured (or Lost)."
                ),
            },
        ),
        (
            "Prospect",
            {
                "fields": ("full_name", "email", "phone", "preferred_contact"),
            },
        ),
        (
            "Investment Intent",
            {
                "fields": (
                    "capital_band",
                    "preferred_tenure",
                    "funding_source",
                    "offering",
                    "notes",
                ),
            },
        ),
        ("Meta", {"fields": ("created_at",)}),
    )

    @admin.display(description="Submitted", ordering="-created_at")
    def submitted_label(self, obj):
        return obj.created_at.strftime("%d %b %Y")

    @admin.display(description="Capital", ordering="capital_band")
    def capital_label(self, obj):
        return obj.get_capital_band_display()

    @admin.display(description="Tenure", ordering="preferred_tenure")
    def tenure_label(self, obj):
        return obj.get_preferred_tenure_display()

    @admin.display(description="Round", ordering="offering")
    def offering_label(self, obj):
        return obj.offering.reference_id if obj.offering else "—"

    @admin.display(description="Status", ordering="status")
    def status_pill(self, obj):
        bg, fg = _INVESTMENT_STATUS_COLOURS.get(obj.status, ("#f1f5f9", "#64748b"))
        return format_html(_pill(obj.get_status_display(), bg, fg))

    def _bulk_set_status(self, request, queryset, new_status, label):
        updated = queryset.update(status=new_status)
        self.message_user(
            request,
            f"{updated} investment inquir{'ies' if updated != 1 else 'y'} marked as {label}.",
        )

    @admin.action(description="Mark selected as Contacted")
    def mark_as_contacted(self, request, queryset):
        self._bulk_set_status(request, queryset, "contacted", "contacted")

    @admin.action(description="Mark selected as Committed")
    def mark_as_committed(self, request, queryset):
        self._bulk_set_status(request, queryset, "committed", "committed")

    @admin.action(description="Mark selected as Funded")
    def mark_as_funded(self, request, queryset):
        self._bulk_set_status(request, queryset, "funded", "funded")

    @admin.action(description="Mark selected as Active")
    def mark_as_active(self, request, queryset):
        self._bulk_set_status(request, queryset, "active", "active")

    @admin.action(description="Mark selected as Matured")
    def mark_as_matured(self, request, queryset):
        self._bulk_set_status(request, queryset, "matured", "matured")

    @admin.action(description="Mark selected as Lost")
    def mark_as_lost(self, request, queryset):
        self._bulk_set_status(request, queryset, "lost", "lost")
