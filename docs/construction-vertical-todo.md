# Construction Vertical — Implementation TODO

> Live tracking document for the build-out of `bejundas.co.tz/construction/` from Coming Soon page to full vertical site.
> Updated as each phase ships. Each phase = its own branch, PR to `develop`, client approval, then next branch begins.

---

## Scope decisions (locked in 2026-05-19)

| Decision | Choice | Rationale |
|---|---|---|
| Model scope | **Option A — Lean core** | 4 models (Service, Project, Testimonial, Certification). Honours ADR-002 — no abandoned shells. `Property`, `Product`, `Equipment` deferred until real content exists for them. |
| Content strategy | **Curated placeholder** | Tanzania-flavoured, plausible, all editable in admin. Real client content replaces row-by-row when ready. |
| Lead form | **Full RFP / Quote request** | Project type, location, scope, budget range, timeline, attachments, admin status workflow. |
| Brand | Charcoal `#2c2c2c` + Orange `#f47920` | Per CLAUDE.md §5 vertical palette. |
| Viora demos | `demo-construction` (homepage) + `demo-corporate` (inner pages) + `demo-architechture` (visual cues) | Per CLAUDE.md §14 mapping. |
| URL | `/construction/` (path-based) | Per ADR-007 — no subdomain. |
| Workflow | 5 stacked PRs, sequential approval | Same cadence as admin overhaul (Phase 5). One phase merges → next branch starts. |

---

## Phase 1 — Scaffold & homepage shell

**Branch:** `feature/construction-phase-1-scaffold`
**Goal:** App exists, routing handed off from `apps.leads`, homepage shell live with charcoal/orange theme.

### Tasks
- [ ] Create `apps/construction/` via `python manage.py startapp construction apps/construction`
- [ ] Update `apps/construction/apps.py` → `ConstructionConfig(name='apps.construction', verbose_name='Construction')`
- [ ] Add `'apps.construction'` to `INSTALLED_APPS` in `config/settings/base.py`
- [ ] Remove construction line from `apps/leads/urls.py` (the `path("construction/", views.coming_soon, ...)` entry)
- [ ] Add `path("construction/", include("apps.construction.urls"))` to `config/urls.py` (above hub urls)
- [ ] Create `apps/construction/urls.py` with `app_name = "construction"` and home route only
- [ ] Create `apps/construction/views.py` with `home` function-based view
- [ ] Copy Viora shared CSS overrides: `cp ../viora/demo-construction/css/* static/construction/css/`
- [ ] Copy Viora images: `cp -r ../viora/demo-construction/images/* static/construction/images/`
- [ ] Copy architecture images for portfolio sections: `cp -r ../viora/demo-architechture/images/* static/construction/images/arch/`
- [ ] Create `apps/construction/templates/construction/base_construction.html` extending `core/base.html`, loading charcoal/orange CSS variables
- [ ] Create `apps/construction/templates/construction/home.html` — port `demo-construction/index.html` body into Django template, rewrite asset paths
- [ ] Wire `app_theme` context processor in `apps/core/context_processors.py` to return charcoal/orange when `resolver_match.app_name == 'construction'`
- [ ] Update `apps/hub/sitemaps.py` — change `("leads:construction", 0.7, "monthly")` to `("construction:home", 0.7, "monthly")`
- [ ] Tests: 1 view test (home returns 200, correct template), 1 routing test
- [ ] Run `ruff check . && black --check . && pytest`
- [ ] Open PR → `develop`, await approval

---

## Phase 2 — Models & admin

**Branch:** `feature/construction-phase-2-models` (off Phase 1 once merged)
**Goal:** 4 core models + Unfold admin entries with thumbnails, status pills, ordering.

### Tasks
- [ ] Create `apps/construction/models.py` with 4 models, all inheriting `apps.core.models.BaseModel`:
  - [ ] `ConstructionService` — name, slug, summary, description (TinyMCE), icon (Material icon name), is_active, order
  - [ ] `Project` — title, slug, sector (choices: residential/commercial/civil/industrial/fitout/renovation), location_city, location_region, year_completed, description, cover_image, is_featured, order
  - [ ] `Testimonial` — author_name, author_role, organisation, quote, is_featured, order
  - [ ] `Certification` — name, issuer, year_awarded, certificate_image (optional), is_active, order
- [ ] Run `makemigrations apps.construction && migrate`
- [ ] Create `apps/construction/admin.py` with Unfold `ModelAdmin` per model:
  - [ ] `ConstructionServiceAdmin` — icon_chip, status_pill, ordering
  - [ ] `ProjectAdmin` — cover_thumbnail (60×40), sector pill (color-coded), year column, status_pill
  - [ ] `TestimonialAdmin` — featured pill, ordering
  - [ ] `CertificationAdmin` — certificate_thumbnail (if uploaded), status_pill, year column
- [ ] Add 4 Unfold sidebar entries under a new "Construction" group in `config/settings/base.py` SIDEBAR config (icons: `engineering`, `domain`, `format_quote`, `verified`)
- [ ] Tests: model `__str__` + `Meta` + custom methods + 1 admin smoke test per model
- [ ] Run `ruff + black + pytest`
- [ ] Open PR → `develop`, await approval

---

## Phase 3 — Inner pages (About, Services, Projects, Project Detail, Contact)

**Branch:** `feature/construction-phase-3-pages` (off Phase 2 once merged)
**Goal:** All inner pages live, ported from `demo-corporate`, skinned charcoal/orange, wired to models.

### Tasks
- [ ] Add URLs: `about/`, `services/`, `projects/`, `projects/<slug>/`, `contact/`
- [ ] Views: `about`, `services_list`, `projects_list` (with sector filter), `project_detail`, `contact` (handles ContactForm submission separately from RFP)
- [ ] Templates ported from `../viora/demo-corporate/` with charcoal/orange skin:
  - [ ] `about.html` — company story, mission, vision, certifications strip
  - [ ] `services.html` — grid of `ConstructionService` cards
  - [ ] `projects.html` — filterable grid (filter chips per sector), `Project` cards with cover image + sector pill + year
  - [ ] `project_detail.html` — hero with cover image, description, sector/location/year meta, related-projects strip
  - [ ] `contact.html` — contact details + simple contact form
- [ ] Update navbar partial — construction-specific nav for inner pages
- [ ] Update sitemap — add static inner pages + dynamic `ProjectSitemap` for project detail URLs
- [ ] Update `app_theme` context for inner pages
- [ ] Tests: 1 status-code test per view, sector filter test for projects list
- [ ] Run `ruff + black + pytest`
- [ ] Open PR → `develop`, await approval

---

## Phase 4 — RFP / Quote request form

**Branch:** `feature/construction-phase-4-rfp` (off Phase 3 once merged)
**Goal:** Full quote-request flow live, email notification working, admin status workflow.

### Tasks
- [ ] Add `QuoteRequest` model to `apps/construction/models.py` with fields:
  - Contact: `full_name`, `company` (blank=True), `email`, `phone`
  - Project basics: `project_type` (choices match `Project.sector`), `location_region`, `location_district`, `estimated_start`
  - Scope: `scope_description` (min 50 chars validated), `budget_range` (choices: <50M / 50-200M / 200M-1B / 1B+ TZS), `timeline` (choices: 1-3 / 3-6 / 6-12 / 12+ months)
  - Status: `status` (new / reviewed / quoted / won / lost / closed), `internal_notes` (admin only)
- [ ] Add `QuoteAttachment` model — FK to `QuoteRequest`, `file` (FileField, validated PDF/JPG/PNG, max 5MB), up to 3 per request
- [ ] Migration
- [ ] Form `QuoteRequestForm` in `apps/construction/forms.py` — `ModelForm`, widget-tweaks classes, multi-file attachment widget
- [ ] View `quote_request` — GET shows form, POST validates + saves + sends email + shows success page
- [ ] URL: `/construction/quote/`
- [ ] Template `quote_request.html` — multi-section form (Contact / Project / Scope / Attachments)
- [ ] Email template `emails/quote_request_notification.html` — formatted HTML email to `LEADS_EMAIL`
- [ ] Admin `QuoteRequestAdmin` with inline `QuoteAttachment`, `status_pill` (color per status), `mark_as_*` actions (mark_as_reviewed / quoted / won / lost / closed), list filter on status + project_type + budget_range
- [ ] Add navbar CTA button "Request a Quote" linking to `/construction/quote/`
- [ ] Tests: form validation (each required field, scope min length, file size, file type), view (GET 200, POST creates record + sends email), admin actions
- [ ] Run `ruff + black + pytest`
- [ ] Open PR → `develop`, await approval

---

## Phase 5 — Curated content seed + polish + reports

**Branch:** `feature/construction-phase-5-polish` (off Phase 4 once merged)
**Goal:** Site looks real, mobile-tested, SEO-ready, reports generated.

### Tasks
- [ ] Data migration `apps/construction/migrations/00XX_seed_curated_content.py`:
  - [ ] 6-8 `ConstructionService` rows — Residential, Commercial, Civil works, MEP, Fit-out, Project management, Design-build, Renovations
  - [ ] 8-10 `Project` rows with Tanzania-flavoured locations (Dar / Arusha / Mwanza / Dodoma / Zanzibar / Mbeya), mixed sectors, years 2021-2025
  - [ ] 3-4 `Testimonial` rows — plausible TZ business names
  - [ ] 3-4 `Certification` rows — NCC class registration, ISO 9001, ISO 14001, OSHA
- [ ] Mobile pass on all construction pages (375 / 768 / 1024 widths)
- [ ] SEO: `{% block title %}` + `{% block meta_description %}` on every page, vertical-specific OG image
- [ ] Add `Project` detail pages to sitemap (`ProjectSitemap` class)
- [ ] Verify charcoal/orange theme is consistent across all pages (no Viora orange leakage from other demos)
- [ ] Update CLAUDE.md §13 phase plan table — mark "Construction" as shipped
- [ ] Run `ruff + black + pytest` (target: 24/24 + new tests still passing)
- [ ] Generate `docs/client/construction-vertical-report.html` (matching phase-5 template)
- [ ] Generate `docs/technical/construction-vertical-report.html` (matching phase-5 template)
- [ ] Open PR → `develop`, await approval
- [ ] After merge: open PR `develop` → `main` for production deploy

---

## Estimated timeline

| Phase | Effort | Cumulative |
|---|---|---|
| Phase 1 — Scaffold | ~1 day | Day 1 |
| Phase 2 — Models & admin | ~1 day | Day 2 |
| Phase 3 — Inner pages | ~2 days | Day 4 |
| Phase 4 — RFP form | ~1.5 days | Day 5-6 |
| Phase 5 — Content seed + polish + reports | ~1.5 days | Day 7-8 |

**Total:** ~1-1.5 weeks at one-phase-per-day cadence.

---

## Deployment plan (after Phase 5 merges to develop)

1. PR `develop` → `main`
2. Merge triggers webhook → cPanel deploy
3. Server runs `migrate apps.construction` (Phases 2, 4 added migrations)
4. Server runs `collectstatic` (new images + CSS in `static/construction/`)
5. Verify `/construction/` returns full site (not Coming Soon)
6. Submit new Project detail URLs to Google Search Console via sitemap re-fetch
7. Update client → "construction vertical is live"

---

## Non-goals (explicit deferrals)

These are **deliberately out of scope** for this build:

- `Property` model (real estate listings) — wait until client confirms property dealings are part of construction vertical
- `Product` model (materials supplier catalogue) — wait until client confirms supplier business
- `Equipment` model (heavy machinery showcase) — nice-to-have, deferred
- Multi-language (Swahili) — deferred to a future i18n pass across the whole platform
- Project timeline / Gantt visualisations — too feature-rich for initial launch
- Client login / project tracking portal — not requested
- Payment integration — not requested

If any of these become real requirements later, each is a separate small PR (~1 day per model + admin).

---

## Reference

- `CLAUDE.md §13` — generic playbook for adding any vertical
- `CLAUDE.md §14` — Viora template mapping table
- `CLAUDE.md §5` — brand palette per vertical
- `ADR-002` — why we wait for real content before building shells
- `ADR-007` — why path-based routing (not subdomains)
- `apps/leads/admin.py` — status_pill pattern reused in this build
- `apps/hub/admin.py` — thumbnail patterns reused in this build
