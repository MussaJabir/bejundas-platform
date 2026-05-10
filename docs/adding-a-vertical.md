# Adding a New Vertical — Playbook

This is the long-form guide for promoting a Coming Soon subdomain to a full vertical Django app. CLAUDE.md §13 has the condensed version; this document expands on each step with code, examples, and gotchas.

---

## When to use this playbook

Use this when a vertical (financial, construction, energies, farming, investments) has:

1. Real, structured content ready (services, products, photos, prices)
2. A content owner assigned
3. A clear deadline to finish populating

If any of those is missing, leave the subdomain on the Coming Soon page. Empty admin shells become abandoned admin shells.

---

## Estimated effort

| Step | Time |
|---|---|
| Branch + scaffold | 30 min |
| Models + migrations | 2-4 hours |
| Views + URLs + forms | 2-4 hours |
| Templates from Viora demo | 1-3 days |
| Admin (Unfold ModelAdmin) | 2-4 hours |
| Tests | 4-8 hours |
| Content fill (admin work) | 1-3 days |
| Review + deploy | 2-4 hours |

**Total: 1-2 weeks per vertical.** The first vertical takes the longest because you discover gaps in the shared infrastructure. Subsequent verticals are faster.

---

## Step-by-step

### Step 1 — Branch from develop

```bash
git checkout develop
git pull origin develop
git checkout -b feature/vertical-financial
```

### Step 2 — Scaffold the Django app

```bash
python manage.py startapp financial apps/financial
```

This creates:
```
apps/financial/
├── __init__.py
├── admin.py
├── apps.py
├── migrations/
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

Edit `apps/financial/apps.py`:

```python
from django.apps import AppConfig


class FinancialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.financial'
    verbose_name = 'Financial Services'
```

### Step 3 — Register the app

In `config/settings/base.py`, add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'apps.core',
    'apps.hub',
    'apps.leads',
    'apps.financial',  # <-- new
]
```

### Step 4 — Switch subdomain routing

In `config/hosts.py`, replace the line that points `financial` to the Coming Soon view:

```python
# before
host(r'financial', 'apps.leads.urls', name='financial-coming-soon'),

# after
host(r'financial', 'apps.financial.urls', name='financial'),
```

### Step 5 — Build models

`apps/financial/models.py`:

```python
from django.db import models
from django.urls import reverse
from apps.core.models import BaseModel


class FinancialProduct(BaseModel):
    PRODUCT_TYPES = [
        ('loan', 'Loan'),
        ('investment', 'Investment'),
        ('insurance', 'Insurance'),
        ('advisory', 'Advisory'),
    ]

    name        = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    summary     = models.CharField(max_length=300)
    description = models.TextField()
    icon_class  = models.CharField(max_length=100, blank=True, default='', help_text='Bootstrap icon class')
    image       = models.ImageField(upload_to='financial/products/', blank=True)
    min_amount  = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_amount  = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_active   = models.BooleanField(default=True)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Financial Product'
        verbose_name_plural = 'Financial Products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('financial:product_detail', kwargs={'slug': self.slug})


class LoanApplication(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    full_name = models.CharField(max_length=200)
    email     = models.EmailField()
    phone     = models.CharField(max_length=20)
    product   = models.ForeignKey(FinancialProduct, on_delete=models.PROTECT, related_name='applications')
    amount    = models.DecimalField(max_digits=12, decimal_places=2)
    purpose   = models.TextField()
    status    = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes     = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Loan Application'
        verbose_name_plural = 'Loan Applications'

    def __str__(self):
        return f'{self.full_name} - {self.product.name}'
```

Run migrations:

```bash
python manage.py makemigrations apps.financial
python manage.py migrate
```

### Step 6 — Views and URLs

`apps/financial/views.py`:

```python
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import FinancialProduct
from .forms import LoanApplicationForm


class FinancialHomeView(TemplateView):
    template_name = 'financial/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['products'] = FinancialProduct.objects.filter(is_active=True)[:6]
        return ctx


class ProductListView(ListView):
    model = FinancialProduct
    template_name = 'financial/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return FinancialProduct.objects.filter(is_active=True)


class ProductDetailView(DetailView):
    model = FinancialProduct
    template_name = 'financial/product_detail.html'
    context_object_name = 'product'


class ApplyView(CreateView):
    form_class = LoanApplicationForm
    template_name = 'financial/apply.html'
    success_url = reverse_lazy('financial:apply_success')

    def form_valid(self, form):
        messages.success(self.request, 'Your application has been submitted. We will contact you within 2 business days.')
        return super().form_valid(form)
```

`apps/financial/urls.py`:

```python
from django.urls import path
from .views import FinancialHomeView, ProductListView, ProductDetailView, ApplyView, ApplySuccessView


app_name = 'financial'

urlpatterns = [
    path('', FinancialHomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('apply/', ApplyView.as_view(), name='apply'),
    path('apply/success/', ApplySuccessView.as_view(), name='apply_success'),
]
```

### Step 7 — Forms

`apps/financial/forms.py`:

```python
from django import forms
from .models import LoanApplication


class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['full_name', 'email', 'phone', 'product', 'amount', 'purpose']
        widgets = {
            'purpose': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        return amount
```

### Step 8 — Templates

Create `apps/financial/templates/financial/`:

- `base_financial.html` — extends `core/base.html`, loads Viora demo-insurance assets, sets brand color
- `home.html`
- `products.html`
- `product_detail.html`
- `apply.html`
- `apply_success.html`

Visual reference: **Viora `demo-insurance/`** ships full pages. Copy the HTML structure into the templates above and replace static content with Django template variables.

For inner pages not in `demo-insurance`, fall back to `demo-corporate` and re-skin with the financial color palette (`#0a2342` primary, `#c9a84c` accent).

Example `apps/financial/templates/financial/base_financial.html`:

```django
{% extends "core/base.html" %}
{% load static %}

{% block extra_head %}
<link rel="stylesheet" href="{% static 'viora/demo-insurance/css/insurance-theme.css' %}">
<style>
    :root {
        --primary: #0a2342;
        --accent:  #c9a84c;
    }
</style>
{% endblock %}

{% block navbar %}
    {% include "core/navbar.html" with current_app="financial" %}
{% endblock %}

{% block footer %}
    {% include "core/footer.html" with current_app="financial" %}
{% endblock %}
```

### Step 9 — Admin

`apps/financial/admin.py`:

```python
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import FinancialProduct, LoanApplication


@admin.register(FinancialProduct)
class FinancialProductAdmin(ModelAdmin):
    list_display = ['name', 'product_type', 'is_active', 'order', 'updated_at']
    list_filter = ['product_type', 'is_active']
    search_fields = ['name', 'summary']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'product_type', 'summary', 'description'),
        }),
        ('Display', {
            'fields': ('icon_class', 'image', 'order', 'is_active'),
        }),
        ('Constraints', {
            'fields': ('min_amount', 'max_amount'),
            'classes': ('collapse',),
        }),
    )


@admin.register(LoanApplication)
class LoanApplicationAdmin(ModelAdmin):
    list_display = ['full_name', 'email', 'product', 'amount', 'status', 'created_at']
    list_filter = ['status', 'product', 'created_at']
    search_fields = ['full_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Applicant', {
            'fields': ('full_name', 'email', 'phone'),
        }),
        ('Application', {
            'fields': ('product', 'amount', 'purpose'),
        }),
        ('Status', {
            'fields': ('status', 'notes'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
```

### Step 10 — Update SiteSettings (optional)

If financial needs editable hero text, banner, etc., extend `apps.core.models.SiteSettings`:

```python
class SiteSettings(BaseModel):
    ...
    # Existing hub fields ...

    # Financial-specific fields
    financial_hero_headline = models.CharField(max_length=200, blank=True, default='')
    financial_hero_subtext  = models.TextField(blank=True, default='')
    financial_apply_cta     = models.CharField(max_length=100, blank=True, default='Apply Now')
```

Then add a proxy admin for the new section:

```python
class FinancialPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Financial Page'
        verbose_name_plural = 'Financial Page'


@admin.register(FinancialPageSettings)
class FinancialPageSettingsAdmin(ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('financial_hero_headline', 'financial_hero_subtext', 'financial_apply_cta'),
        }),
    )

    def changelist_view(self, request, extra_context=None):
        return HttpResponseRedirect(reverse('admin:core_financialpagesettings_change', args=[1]))
```

If `SiteSettings` grows past ~30 vertical-specific fields, switch to a per-vertical settings model:

```python
# apps/financial/models.py
class FinancialSiteSettings(BaseModel):
    hero_headline = models.CharField(max_length=200, blank=True, default='')
    # ... etc
```

### Step 11 — Tests

`apps/financial/tests/test_models.py`:

```python
import pytest
from apps.financial.models import FinancialProduct


@pytest.mark.django_db
def test_product_str():
    product = FinancialProduct.objects.create(
        name='Personal Loan',
        slug='personal-loan',
        product_type='loan',
        summary='Personal loans up to TZS 10M',
        description='Description here.',
    )
    assert str(product) == 'Personal Loan'
```

`apps/financial/tests/test_views.py`:

```python
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('financial:home'), HTTP_HOST='financial.bejundas.local')
    assert response.status_code == 200
    assert 'financial/home.html' in [t.name for t in response.templates]
```

Aim for 80% coverage on the new app.

### Step 12 — Run checks

```bash
ruff check .
black --check .
pytest apps/financial/
```

### Step 13 — Commit, push, PR

```bash
git add apps/financial/ config/hosts.py config/settings/base.py
git commit -m "feat(financial): launch financial vertical with products and loan applications"
git push -u origin feature/vertical-financial

gh pr create --base develop --title "feat(financial): launch financial vertical" --body "..."
```

### Step 14 — Review, merge to develop, then merge develop to main

Standard flow per [docs/branching.md](branching.md).

### Step 15 — Deploy

Webhook fires automatically on merge to `main`. Verify:

- `https://financial.bejundas.co.tz/` loads the new app, not Coming Soon
- Admin at `https://bejundas.co.tz/admin/` shows Financial Products and Loan Applications sections
- Submit a test application; verify email arrives at `LEADS_EMAIL` or `CONTACT_EMAIL`

### Step 16 — Update SESSION_LOG.md

Append:

```markdown
## Session N — YYYY-MM-DD EAT

**Goal:** Launch financial vertical.
**Branch:** feature/vertical-financial
**Status:** Complete

### What Was Done
- ...

### Files Changed
| File | Action | Notes |
|---|---|---|
| ... | ... | ... |

### Decisions Made
- ...

### Next Session Should
- [ ] ...
```

### Step 17 — Remove the Coming Soon record (optional)

Once financial is live, decide:
- Keep the `VerticalPlaceholder` record for `financial` in case you ever need to put the Coming Soon page back
- Or delete it from admin to keep the placeholder list clean

---

## Verticals 2-N: what changes

For the second vertical onward, the shared infrastructure (BaseModel, SiteSettings, admin theme, deploy, base templates) is already proven. The work narrows to:

- New models specific to that vertical
- New views, URLs, forms, templates from the matching Viora demo
- New admin registrations
- New tests
- Update `config/hosts.py` and `INSTALLED_APPS`

The first vertical typically reveals 3-5 gaps in the shared infrastructure (e.g. missing template tag, missing context variable). Fix those in `apps.core` and the gaps stay fixed forever.

---

## Common gotchas

| Gotcha | Cause | Fix |
|---|---|---|
| Subdomain still shows Coming Soon after deploy | Forgot to update `config/hosts.py` | Update host pattern, redeploy |
| Static files 404 on subdomain | Viora assets not in `STATICFILES_DIRS` | Add path, run `collectstatic` |
| Admin section doesn't appear | App not in `INSTALLED_APPS` or `admin.py` not discovered | Verify both; restart Passenger |
| `NoReverseMatch` for `financial:home` | URL namespace not set | Add `app_name = 'financial'` in `urls.py` |
| Form submission redirects to wrong domain | `success_url` is absolute path, hits `bejundas.co.tz` instead of `financial.bejundas.co.tz` | Use `django-hosts` `host_url` template tag, or use `reverse_lazy` with `host` kwarg |
| Admin styling broken on new pages | New app templates don't inherit from `core/base.html` | Always extend `core/base.html` (or your `base_<vertical>.html` which extends `core/base.html`) |
