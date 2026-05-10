# CLAUDE.md — Bejundas Platform

> Master project instructions for Claude Code.
> Read this entire file before doing anything in this repo.
> When in doubt, check this file first, then ask.

---

## 1. Project Identity

**Client:** Bejundas Group of Companies
**Repo:** [github.com/MussaJabir/bejundas-platform](https://github.com/MussaJabir/bejundas-platform)
**Primary domain:** `bejundas.co.tz`
**Stack:** Django 5.x LTS + MySQL + cPanel + Phusion Passenger + GitHub Actions
**Started:** 2026-05-10
**Target launch:** End of May 2026 (~2 weeks from start)

### What this project is

A multi-subdomain Django web platform serving Bejundas Group's six business verticals plus a parent landing site. Built as a **monorepo** — one Django project, one Passenger app, one deploy — with subdomain routing handled by `django-hosts`.

### Subdomain map

| Subdomain | Status (MVP) | Django app |
|---|---|---|
| `bejundas.co.tz` | Full marketing site | `apps.hub` |
| `financial.bejundas.co.tz` | Coming Soon page | `apps.leads.coming_soon` |
| `construction.bejundas.co.tz` | Coming Soon page | `apps.leads.coming_soon` |
| `energies.bejundas.co.tz` | Coming Soon page | `apps.leads.coming_soon` |
| `farming.bejundas.co.tz` | Coming Soon page | `apps.leads.coming_soon` |
| `investments.bejundas.co.tz` | Coming Soon page | `apps.leads.coming_soon` |
| `technologies.bejundas.co.tz` | 301 redirect to `bjptechnologies.co.tz` | redirect view |

`bjptechnologies.co.tz` is a separate live site in the [bjp-technologies-web](https://github.com/MussaJabir/bjp-technologies-web) repo. It is **not** part of this monorepo.

---

## 2. Architecture Decision Record

This section explains *why* the architecture is what it is. Read it before proposing changes.

### ADR-001: Monorepo over six separate repos

**Decision:** Single Django project, multiple apps, `django-hosts` for routing.

**Why:**
- cPanel + Passenger handles wildcard subdomains via "Share document root" toggle. One Passenger app serves all subdomains cleanly.
- Six separate repos means six webhook deploys, six virtualenvs, six SSL renewals, six CI pipelines. Unmaintainable for a solo developer.
- Shared code (base templates, Lead model, admin theme, deploy pipeline) lives in one place.

**Trade-off:** A bug in shared code can break all subdomains at once. Mitigated by CI tests and staged deploys.

### ADR-002: Hub-only MVP

**Decision:** Build the hub site fully. The five verticals get a single shared "Coming Soon" page themed per subdomain via a `VerticalPlaceholder` admin record.

**Why:**
- Client confirmed no real content exists for any vertical at MVP time.
- Building 6 vertical-specific apps with placeholder content creates 6 abandoned shells.
- Coming Soon + lead capture form turns each subdomain into a marketing asset that converts visitors into a `Lead` row, which is more valuable than a fake services page.
- Verticals are added later when content is ready (see §13 Adding a New Vertical).

**Trade-off:** Subdomains do not show full vertical-specific content at launch. Acceptable because no real content exists to show.

### ADR-003: MySQL for both dev and production

**Decision:** Use MySQL/MariaDB locally and on cPanel. Do not use SQLite for development.

**Why:**
- cPanel only supports MySQL/MariaDB. PostgreSQL is not available.
- SQLite-in-dev / MySQL-in-prod creates surprises (charset, JSONField behavior, case sensitivity, index limits). Lessons learned from `bjp-technologies-web`.

**Trade-off:** Slightly more setup for new developers (must install MySQL locally). Acceptable.

### ADR-004: No custom user model with `app_access` field

**Decision:** Use `AbstractUser` directly. No `app_access JSONField`. No multi-app account switching.

**Why:**
- Public verticals do not require user accounts at MVP.
- Admin users use Django's built-in `Group` system for per-app permissions.
- Premature schema = expensive migrations later when actual requirements crystallize.

**Trade-off:** If a vertical later needs end-user accounts, that vertical adds its own user-related models. We cross that bridge then.

### ADR-005: One themed Unfold admin, not seven AdminSite subclasses

**Decision:** Use `django-unfold` with per-app accent colors injected via context. Do not subclass `AdminSite` per vertical.

**Why:**
- Custom `AdminSite` subclasses break Django's admin URL registry and double maintenance cost.
- Unfold's existing theming covers per-section branding.
- Already proven on `bjp-technologies-web`.

**Trade-off:** All admins share one URL prefix. Acceptable.

### ADR-006: Deploy via GitHub webhook to cPanel

**Decision:** GitHub webhook → Django endpoint → detached shell script. No SSH, no cPanel UAPI.

**Why:**
- Hosting provider blocks SSH (port 22) and cPanel UAPI (port 2083) externally.
- Lessons learned from `bjp-technologies-web` Session 13.

**Trade-off:** Requires `GITHUB_WEBHOOK_SECRET` env var on server. HMAC validation in webhook handler.

---

## 3. Technology Stack

| Layer | Choice | Notes |
|---|---|---|
| Language | Python 3.11 | cPanel-supported version |
| Framework | Django 5.x LTS | Stability over Django 6 |
| Database | MySQL 8 / MariaDB | `utf8mb4` charset always |
| Routing | `django-hosts` | Subdomain → URLConf mapping |
| Admin | `django-unfold` | Themed admin |
| Forms | `django-widget-tweaks` | Lighter than crispy-forms |
| Env vars | `django-environ` | Loaded in `manage.py` and `passenger_wsgi.py` |
| Static | `whitenoise` | Served by Django |
| Editor | TinyMCE (Unfold built-in) | Avoid CKEditor 4 (EOL) |
| Auth | None at MVP | Only admin users |
| Server | cPanel + Passenger (WSGI) | `passenger_wsgi.py` entry |
| CI | GitHub Actions | Tests on every push/PR |
| Deploy | GitHub webhook → Django endpoint → shell script | See `apps/core/webhook.py` |
| Linting | `ruff` + `black` | Enforced in CI |
| Testing | `pytest` + `pytest-django` + `factory_boy` | 80% coverage target |

### Frontend

- Bootstrap 5 (via Viora template)
- Vanilla JS (jQuery only where Bootstrap requires it)
- Viora HTML5 template — `demo-corporate` for hub, others picked per vertical when built (§14)

---

## 4. Directory Structure

```
bejundas-platform/
├── CLAUDE.md                       This file
├── SESSION_LOG.md                  Append-only session log
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── SECURITY.md
├── LICENSE                         Proprietary, all rights reserved
├── manage.py
├── passenger_wsgi.py               cPanel Passenger entry point
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml                  ruff + black config
├── pytest.ini
├── .env.example                    Template for .env
├── .env                            Local secrets (gitignored)
├── .gitignore
├── .cpanel.yml                     Post-deploy tasks
│
├── .github/
│   ├── workflows/
│   │   └── deploy.yml              CI: ruff + black + pytest
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
│
├── docs/
│   ├── deployment.md               cPanel + webhook deploy guide
│   ├── branching.md                Git workflow details
│   ├── database.md                 MySQL setup, migration rules
│   └── adding-a-vertical.md        Step-by-step playbook for verticals 2-6
│
├── config/                         Django project settings
│   ├── __init__.py
│   ├── hosts.py                    django-hosts patterns
│   ├── urls.py                     Root URL conf (hub urls)
│   ├── wsgi.py
│   ├── asgi.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py                 Shared settings
│       ├── development.py          Local dev (DEBUG=True)
│       ├── production.py           cPanel production
│       └── ci.py                   GitHub Actions test runs
│
├── apps/
│   ├── core/                       Shared base + deploy
│   │   ├── models.py               BaseModel, SiteSettings (singleton)
│   │   ├── admin.py                SiteSettings + proxy admin pattern
│   │   ├── views.py                Health check
│   │   ├── webhook.py              GitHub deploy webhook receiver
│   │   ├── context_processors.py   company_info, app_theme
│   │   ├── templatetags/
│   │   ├── templates/core/
│   │   │   ├── base.html
│   │   │   ├── navbar.html
│   │   │   └── footer.html
│   │   └── tests/
│   │
│   ├── hub/                        bejundas.co.tz marketing site
│   │   ├── models.py               News, TeamMember, Service summary
│   │   ├── views.py                home, about, services, news, team, contact
│   │   ├── urls.py
│   │   ├── forms.py                ContactForm
│   │   ├── templates/hub/
│   │   │   ├── home.html
│   │   │   ├── about.html
│   │   │   ├── services.html
│   │   │   ├── news.html
│   │   │   ├── team.html
│   │   │   └── contact.html
│   │   └── tests/
│   │
│   └── leads/                      Lead model + Coming Soon view
│       ├── models.py               Lead, VerticalPlaceholder
│       ├── views.py                coming_soon (themed by host)
│       ├── urls.py
│       ├── forms.py                LeadForm
│       ├── admin.py
│       ├── templates/leads/
│       │   └── coming_soon.html    One template, themed via VerticalPlaceholder record
│       └── tests/
│
├── static/
│   ├── viora/                      Viora SHARED assets only (css, js, fonts, icons, images, favicon)
│   │                               Copied from ../viora/assets/ during Phase 1. Read-only.
│   │                               Demo HTML files are NOT copied here — they are ported
│   │                               into Django templates by hand (see §14).
│   ├── hub/                        Per-app static (demo-specific CSS override + images)
│   │   ├── css/                    e.g. corporate.css from viora/demo-corporate/css/
│   │   └── images/                 e.g. hero shots from viora/demo-corporate/images/
│   ├── css/
│   │   └── bejundas.css            Custom global overrides
│   ├── js/
│   │   └── bejundas.js
│   └── images/                     Brand logo, favicons, OG images
│
├── templates/
│   ├── base.html                   Master base
│   ├── 404.html
│   └── 500.html
│
├── public/
│   ├── static/                     collectstatic output (gitignored)
│   └── media/                      User uploads (gitignored)
│
├── scripts/
│   └── deploy.sh                   Detached deploy script run by webhook
│
└── tmp/
    └── restart.txt                 Touch to restart Passenger
```

---

## 5. Brand & Design System

### Hub colors (bejundas.co.tz)

```css
--primary:    #1a1a2e;
--accent:     #e94560;
--bg:         #ffffff;
--text:       #2c2c2c;
```

### Per-vertical color tokens

These are stored in the `VerticalPlaceholder` model (admin-editable) so the Coming Soon page can be re-themed without code changes. Defaults below.

| Vertical | Primary | Accent | Viora demo (when built) |
|---|---|---|---|
| Financial | `#0a2342` | `#c9a84c` | `demo-insurance` |
| Construction | `#2c2c2c` | `#f47920` | `demo-construction` + `demo-architechture` |
| Energies | `#0d3b2e` | `#f9c41a` | `demo-solarenergy` |
| Farming | `#2d5a27` | `#8bc34a` | `demo-agriculturefarming` |
| Investments | `#1a0533` | `#d4af37` | `demo-agency` |
| Technologies | n/a (redirect) | n/a | n/a (lives in `bjp-technologies-web`) |

### Typography

- Headings: per Viora demo (varies)
- Body: per Viora demo
- Override only if client provides brand fonts

---

## 6. Django Conventions

### Models

- All models inherit from `apps.core.models.BaseModel`:
  ```python
  class BaseModel(models.Model):
      id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)

      class Meta:
          abstract = True
  ```
- Always define `__str__`, `Meta.verbose_name`, `Meta.verbose_name_plural`
- Never use `null=True` on string fields. Use `blank=True, default=''`
- Use `choices` for any field with a fixed set of values

### Views

- Class-based views for CRUD/list/detail
- Function-based views only for simple one-offs
- Always use `get_object_or_404` over raw `.get()`
- Every view has a named URL

### URLs

- Pattern: `appname:action` (e.g. `hub:home`, `leads:submit`)
- Use `{% url 'appname:action' %}` in templates — never hardcode

### Templates

- All extend `core/base.html`
- Define blocks: `title`, `meta_description`, `extra_head`, `content`, `extra_js`
- `{% load static %}` at the top
- No business logic in templates

### Forms

- Live in `forms.py` per app
- Use `ModelForm` where possible
- `{% csrf_token %}` on every form
- Validate in form's `clean()`, not in the view

### Admin

- Register every model
- `list_display`, `search_fields`, `list_filter` on every `ModelAdmin`
- Group fields with `fieldsets`
- Use Unfold's `ModelAdmin` base class

### SiteSettings singleton (lifted from bjp-tech)

All editable site-wide content lives in `apps.core.models.SiteSettings` — singleton (always pk=1). Access via `SiteSettings.get()`. Passed to every template as `{{ company }}` by `apps.core.context_processors.company_info`.

To add a new editable section:
1. Add fields to `SiteSettings`
2. Create a proxy model
3. Register a proxy admin with `changelist_view` redirecting to the singleton change form
4. Add sidebar link in Unfold config
5. Wire `{{ company.field }}` in template
6. `makemigrations` + `migrate`

---

## 7. Database Rules

- Database: `bejundas_db` (cPanel may prefix the username — adjust in `.env`)
- User: `bejundas_dbuser`
- Host: `localhost`
- Port: `3306`
- Charset: `utf8mb4` always
- Collation: `utf8mb4_unicode_ci`
- Never `migrate --fake` without a comment explaining why
- Never delete a migration file
- Never edit a migration that has been applied to production
- Renaming a field: add new field, copy data, deprecate old field. Never rename directly in MySQL — index rebuilds are expensive

---

## 8. Git Branching Workflow

Non-negotiable. See `docs/branching.md` for details.

```
main           Production. Protected. No direct commits.
develop        Integration branch.
feature/*      New features
fix/*          Bug fixes
hotfix/*       Emergency production fixes (branched from main)
chore/*        Non-code (deps, configs, CI)
docs/*         Documentation
```

### Rules

1. Never commit directly to `main` or `develop`
2. Every task starts with a new branch from `develop`
3. Branch names are lowercase, hyphen-separated, prefixed with type
4. Conventional Commits format
5. CI must pass before merging to `develop`
6. PR review required before merging `develop` to `main`
7. Delete the feature branch after merge

### Conventional Commits

```
type(scope): short description

[optional body]
[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`

Examples:
```
feat(hub): add contact form with email notification
fix(leads): correct VerticalPlaceholder fallback when host unknown
chore(deps): pin Django to 5.1.4
ci(deploy): switch to webhook deploy after SSH blocked
```

---

## 9. CI/CD Pipeline

### `.github/workflows/deploy.yml`

Tests-only workflow. Deploy is triggered separately by GitHub webhook → cPanel.

- Runs on push to `main`, `develop`, and on every PR
- Spins up MySQL 8 service
- Installs `requirements.txt` + `requirements-dev.txt`
- Runs `ruff check .`
- Runs `black --check .`
- Runs `pytest --tb=short`

### Deploy

Merge to `main` → GitHub sends webhook to `https://bejundas.co.tz/deploy/webhook/` → `apps.core.webhook` validates HMAC signature → spawns detached `scripts/deploy.sh` → git pull, pip install, migrate, collectstatic, touch `tmp/restart.txt`.

Required server env: `GITHUB_WEBHOOK_SECRET`.
Required GitHub repo secret: same value, configured under Settings → Webhooks.

---

## 10. Environment Variables

`.env` is gitignored. `.env.example` is the template.

| Variable | Required | Notes |
|---|---|---|
| `SECRET_KEY` | yes | Django secret |
| `DEBUG` | yes | `True` in dev, `False` in prod |
| `ALLOWED_HOSTS` | yes | Comma-separated. Include all 7 hostnames |
| `PARENT_HOST` | yes | `bejundas.co.tz` |
| `DB_NAME` | yes | |
| `DB_USER` | yes | |
| `DB_PASS` | yes | |
| `DB_HOST` | yes | `localhost` on cPanel |
| `DB_PORT` | yes | `3306` |
| `EMAIL_HOST` | yes | SMTP server |
| `EMAIL_PORT` | yes | `587` for STARTTLS |
| `EMAIL_HOST_USER` | yes | |
| `EMAIL_HOST_PASSWORD` | yes | App password, not account password |
| `DEFAULT_FROM_EMAIL` | yes | `Bejundas <info@bejundas.co.tz>` |
| `CONTACT_EMAIL` | yes | Where contact form goes |
| `LEADS_EMAIL` | yes | Where Coming Soon callback leads go |
| `GITHUB_WEBHOOK_SECRET` | prod only | HMAC secret for deploy webhook |

### Rules

- Load in `manage.py` and `passenger_wsgi.py` via `django-environ`
- `DEBUG` must be `False` in production. CI checks for this.
- Never commit `.env`. Public repo means leaks are permanent.

---

## 11. Testing Standards

- Every model: test for `__str__`, `save()`, custom methods
- Every view: status code, template used, authenticated/unauthenticated paths
- Every form: valid data, invalid data, each required field
- Use `pytest-django` fixtures over `unittest.TestCase`
- Use `factory_boy` for test data
- CI uses MySQL 8 service container — same as production
- Coverage target: 80%

---

## 12. Phase Plan

| Phase | Name | Status | Target |
|---|---|---|---|
| Phase 0 | Infrastructure & cPanel setup | In Progress | Day 1 |
| Phase 1 | Repo scaffold & Django bootstrap | TODO | Day 1-2 |
| Phase 2 | Hub site (home, about, services, news, team, contact) | TODO | Day 2-6 |
| Phase 3 | Coming Soon system (5 placeholder subdomains) | TODO | Day 7 |
| Phase 4 | Webhook deploy + CI + first production push | TODO | Day 8-10 |
| Phase 5 | Polish, mobile, SEO, soft launch | TODO | Day 11-14 |

### Phase 0 — Infrastructure (client/dev does this in cPanel)

1. MySQL: create `bejundas_db` + user + grant ALL privileges
2. Domains: create 6 subdomains (`financial`, `construction`, `energies`, `farming`, `investments`, `technologies`) each with **"Share document root with bejundas.co.tz" ON**
3. Setup Python App: Python 3.11, app root `bejundas_platform`, URL `bejundas.co.tz`, startup file `passenger_wsgi.py`, entry point `application`
4. SSL/TLS: AutoSSL on for all 7 hostnames
5. (Optional but recommended) Cloudflare in front for caching + free wildcard SSL fallback

### Phase 1 — Repo scaffold (Claude does)

1. Create `develop` branch from `main`
2. Django project init in `config/`, settings split (`base`, `development`, `production`, `ci`)
3. `requirements.txt`, `requirements-dev.txt`, `pyproject.toml`, `pytest.ini`
4. `.env.example`, `.gitignore`, `manage.py`, `passenger_wsgi.py`
5. `apps/core/` with `BaseModel`, `SiteSettings`, webhook, context processors, base templates
6. `django-hosts` config in `config/hosts.py`
7. Unfold admin wired with brand theme
8. First passing test, first green CI run

### Phase 2 — Hub site

1. `apps/hub/` models: `News`, `TeamMember`, `Service` (summary card)
2. Views: home, about, services, news, news_detail, team, contact
3. Forms: `ContactForm`
4. Templates ported from Viora `demo-corporate`
5. Navbar + footer partials in `apps/core/templates/core/`
6. SiteSettings sections wired via proxy admins (hero, about, services, contact, footer)
7. Tests for each view + ContactForm

### Phase 3 — Coming Soon

1. `apps/leads/` models: `Lead`, `VerticalPlaceholder`
2. Seed 5 `VerticalPlaceholder` rows (financial, construction, energies, farming, investments) with default colors and copy
3. View: `coming_soon` reads `request.get_host()`, fetches matching `VerticalPlaceholder`, renders themed template
4. Form: `LeadForm` with `vertical` set automatically from host
5. Template: one `coming_soon.html` with CSS variables driven by placeholder record
6. Email notification on lead submit
7. Tests for view, form, lead creation

### Phase 4 — Deploy

1. `apps/core/webhook.py` — HMAC validation, spawn detached shell script
2. `scripts/deploy.sh` — git pull, pip install, migrate, collectstatic, restart
3. `.cpanel.yml` for any cPanel-side post-deploy tasks
4. `.github/workflows/deploy.yml` — tests only (deploy is webhook-triggered, not Actions-triggered)
5. First production push, verify webhook fires, verify deploy completes
6. Configure `GITHUB_WEBHOOK_SECRET` in repo settings + server `.env`

### Phase 5 — Polish

1. Mobile pass on all hub pages
2. SEO: meta tags, OG cards, sitemap.xml, robots.txt
3. 404, 500 templates
4. Cloudflare DNS + page rules
5. Soft launch — share with client for review
6. Fill SiteSettings with real client copy
7. Public launch

---

## 13. Adding a New Vertical (Playbook)

When the client says "financial is ready, build it", follow these steps. Each new vertical takes ~1-2 weeks because the architecture, deploy, admin, and base templates already exist.

### Step 1 — Branch

```bash
git checkout develop
git pull
git checkout -b feature/vertical-financial
```

### Step 2 — Create the Django app

```bash
python manage.py startapp financial apps/financial
```

Update `apps/financial/apps.py`:
```python
class FinancialConfig(AppConfig):
    name = 'apps.financial'
    verbose_name = 'Financial Services'
```

### Step 3 — Add to `INSTALLED_APPS`

In `config/settings/base.py`:
```python
INSTALLED_APPS = [
    ...
    'apps.financial',
]
```

### Step 4 — Switch routing

In `config/hosts.py`:
```python
host(r'financial', 'apps.financial.urls', name='financial'),
```

(Replace the previous line that pointed `financial` to `apps.leads.coming_soon`.)

### Step 5 — Build models

Inherit from `BaseModel`. Examples for financial:
```python
class FinancialProduct(BaseModel):
    name        = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True)
    summary     = models.TextField()
    description = models.TextField()
    icon        = models.CharField(max_length=100, blank=True, default='')
    is_active   = models.BooleanField(default=True)
    order       = models.PositiveIntegerField(default=0)

class LoanApplication(BaseModel):
    full_name   = models.CharField(max_length=200)
    email       = models.EmailField()
    phone       = models.CharField(max_length=20)
    product     = models.ForeignKey(FinancialProduct, on_delete=models.PROTECT)
    amount      = models.DecimalField(max_digits=12, decimal_places=2)
    status      = models.CharField(max_length=20, choices=[...], default='pending')
    notes       = models.TextField(blank=True, default='')
```

Run `makemigrations apps.financial && migrate`.

### Step 6 — Views, URLs, forms, templates

Pattern mirrors `apps.hub`. Use the matching Viora demo (§14):

| Vertical | Viora demo |
|---|---|
| Financial | `demo-insurance` |
| Construction | `demo-construction` + `demo-architechture` |
| Energies | `demo-solarenergy` |
| Farming | `demo-agriculturefarming` |
| Investments | `demo-agency` |

For verticals where Viora only ships an `index.html` (most of them), port inner pages (about, services, contact, blog) from `demo-corporate` and re-skin with the vertical's color palette.

### Step 7 — Admin

Register models with Unfold `ModelAdmin`. Use the per-app accent color (set in `VerticalPlaceholder` record) for visual consistency.

### Step 8 — SiteSettings extension

Add vertical-specific fields to `SiteSettings` (e.g. `financial_hero_headline`, `financial_apply_cta`) OR create a per-vertical settings model `FinancialSiteSettings(BaseModel)` if the field count grows past ~15.

### Step 9 — Tests

Every new model, view, form gets tests. CI must pass.

### Step 10 — PR, merge, deploy

```bash
git add .
git commit -m "feat(financial): launch financial vertical with products and loan application"
git push -u origin feature/vertical-financial
```

Open PR to `develop`. Merge after review. Merge `develop` to `main`. Webhook fires. Deploy completes. Live in ~5 minutes.

### Step 11 — Update SESSION_LOG.md

Append a session entry with: what was built, files changed, decisions, next steps.

---

## 14. Viora Template Mapping

### Where the Viora source lives

The Viora HTML5 template lives **outside this repo** at `../viora/` on the dev machine —
i.e. `/home/j4bir/Dev/BJP/Projects/Web/Bejundas Website/viora/`. It is **never copied
into the repo wholesale**.

### How Viora is used (the workflow)

Three things happen, in this order:

**1. Shared assets — copied once during Phase 1.**

`viora/assets/` (Bootstrap CSS/JS, animate.css, swiper, magnific-popup, fonts, icomoon icons,
favicon, shared images) is copied **once** into `static/viora/`. Every Viora-styled page
references these via `{% load static %}` and `{% static 'viora/css/styles.css' %}`.
This is the only Viora content that lives in the repo wholesale.

```bash
mkdir -p static/viora
cp -r ../viora/assets/* static/viora/
```

**2. Per-app demo extras — copied when each app is built.**

Each Viora demo has its own small CSS override file (`demo-corporate/css/corporate.css`,
`demo-insurance/css/insurance.css`, etc.) and a demo-specific `images/` folder.
When an app is built, copy **only those two things** into the app's static folder.
Do not copy the demo's HTML files.

Example for hub (uses `demo-corporate`):
```bash
mkdir -p static/hub/css static/hub/images
cp ../viora/demo-corporate/css/corporate.css   static/hub/css/
cp -r ../viora/demo-corporate/images/*         static/hub/images/
```

Then in `apps/hub/templates/hub/base_hub.html`:
```django
{% load static %}
<link rel="stylesheet" href="{% static 'viora/css/styles.css' %}">
<link rel="stylesheet" href="{% static 'hub/css/corporate.css' %}">
<img src="{% static 'hub/images/hero.jpg' %}" alt="">
```

**3. HTML files are ported by hand — never copied.**

The actual Viora demo HTML files (`index.html`, `about-us.html`, `services.html`, ...)
are **reference material**. Each one becomes a Django template by hand:

- Open the source file (e.g. `../viora/demo-corporate/about-us.html`)
- Copy only the markup inside `<body>` (or the relevant section)
- Save as a Django template (e.g. `apps/hub/templates/hub/about.html`)
- Wrap with `{% extends "core/base.html" %}` and `{% block content %}...{% endblock %}`
- Add `{% load static %}` at the top
- Rewrite all `href="../assets/css/foo.css"` paths to `href="{% static 'viora/css/foo.css' %}"`
- Rewrite all demo-specific paths like `href="css/corporate.css"` to `href="{% static 'hub/css/corporate.css' %}"`
- Replace static content with Django variables: `<h1>About Us</h1>` → `<h1>{{ company.about_headline }}</h1>`

The `viora/` source folder stays at `../viora/` on the dev machine. It is **not committed**
to git. Only the curated subsets in `static/viora/` and `static/<app>/` are committed.

### Demo selection per subdomain

Viora demos vary in completeness. Most are `index.html` only. `demo-corporate`, `demo-agency`,
`demo-medical`, `demo-spasalon`, `demo-insurance` ship full page sets.

| Subdomain | Primary demo | Inner pages source | Notes |
|---|---|---|---|
| Hub | `demo-corporate` | self | Full page set. Use as visual master. |
| Financial | `demo-insurance` | self | Full page set. Reads as financial-services. |
| Construction | `demo-construction` (home) | port from `demo-corporate`, sections from `demo-architechture` | Homepage only. |
| Energies | `demo-solarenergy` (home) | port from `demo-corporate` | Homepage only. |
| Farming | `demo-agriculturefarming` (home) | port from `demo-corporate` + `demo-gardenlandscaping` for visuals | Homepage only. |
| Investments | `demo-agency` (full) + visual cues from `demo-corporate` | self | Don't use luxury/hospitality demo. Agency template re-skinned to gold/dark works better. |
| Technologies | n/a | n/a | 301 redirect to `bjptechnologies.co.tz`. Lives in separate repo. |

Once copied into the repo, the Viora **shared assets** live in `static/viora/` and must not be
modified. Per-app demo CSS overrides live in `static/<app>/css/`. Custom global tweaks go in
`static/css/bejundas.css`. The Viora demo HTML files themselves never enter the repo — they
are read from `../viora/` as reference material when porting templates by hand.

---

## 15. Coding Conventions

- English for all code, comments, commits, docs
- Run `ruff check .` and `black --check .` before committing
- Run `pytest` before opening a PR
- All apps live under `apps/` — import as `from apps.hub.models import ...`
- All shared code lives under `apps.core/` — no separate `shared/` folder
- Models always have `__str__`, `Meta.verbose_name`, `Meta.verbose_name_plural`
- Class-based views by default
- Forms use `django-widget-tweaks` for class control in templates
- Never hardcode colors — use CSS variables
- Template blocks: `title`, `meta_description`, `extra_head`, `content`, `extra_js`
- Every form-handling view that requires login uses `LoginRequiredMixin`
- Admin: `list_display`, `list_filter`, `search_fields` minimum

---

## 16. Don'ts

- Don't add `null=True` to `CharField` / `TextField`
- Don't bypass `BaseModel` — every model inherits it
- Don't subclass `AdminSite` per app
- Don't add `app_access` JSONField or any premature multi-app user logic
- Don't use CKEditor 4 (EOL, security risk)
- Don't use SQLite in dev — match production with MySQL
- Don't commit `.env`, `db.sqlite3`, `public/static/`, `public/media/`, `__pycache__/`
- Don't push directly to `main` or `develop`
- Don't `git push --force` to `main` or `develop` ever
- Don't run `migrate --fake` without a comment explaining why
- Don't edit applied migrations
- Don't hardcode subdomain hostnames in views — read from `request.get_host()`
- Don't introduce new third-party packages without updating `requirements.txt` and CLAUDE.md §3
- Don't create documentation files outside this repo's `docs/` folder
- Don't merge a PR with failing CI

---

## 17. Quick Reference

### Run locally

```bash
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python manage.py migrate
python manage.py runserver
```

To test subdomain routing locally, edit `/etc/hosts`:
```
127.0.0.1   bejundas.local
127.0.0.1   financial.bejundas.local
127.0.0.1   construction.bejundas.local
127.0.0.1   energies.bejundas.local
127.0.0.1   farming.bejundas.local
127.0.0.1   investments.bejundas.local
127.0.0.1   technologies.bejundas.local
```

Then visit `http://bejundas.local:8000` and `http://financial.bejundas.local:8000`.

### Run tests

```bash
pytest
ruff check .
black --check .
```

### Deploy

Merge to `main`. Webhook handles the rest. Watch `/tmp/bjp_deploy.log` on the server.

---

## 18. References

- bjp-technologies-web (sister repo, lessons learned): https://github.com/MussaJabir/bjp-technologies-web
- django-hosts: https://django-hosts.readthedocs.io/
- django-unfold: https://unfoldadmin.com/
- Viora HTML5 template: in `static/viora/`
