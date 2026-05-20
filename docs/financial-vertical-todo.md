# Financial Vertical — Implementation Plan

> Build the `bejundas.co.tz/financial/` vertical for **BEJUNDAS FINANCIAL SERVICES LTD**.
> Replaces the current `apps.leads.coming_soon` route at `/financial/`.
> Stacked PRs into `develop`. Each phase waits for explicit approval before the next starts.

---

## Scope — Locked-In Decisions

| # | Decision | Rationale |
|---|---|---|
| 1 | **Safe regulatory wording** — frame products as "private placement / capital partnership", indicative not guaranteed returns, footer disclaimer stating non-deposit / non-CMSA-registered / non-DIB-insured | Posters say "Expected NOT Taxable" — we mirror that caution. Public website amplifies legal exposure beyond a WhatsApp Status post |
| 2 | **Two lead models** — `LoanInquiry` (microfinance funnel) + `InvestmentInquiry` (capital partner funnel). Distinct admin workflows. | Loan applicants and investment partners are different humans with different sales motions and status pipelines |
| 3 | **Forms shipped fully** — back office confirmed ready by client | Submitter expects a response; we own the obligation only when the workflow on the other side can fulfil it |
| 4 | **Per-vertical legal entity name** — already merged in `fix/per-vertical-legal-names` (PR #48) | Navbar + footer now driven by `app_theme.legal_name`. Financial inherits `BEJUNDAS FINANCIAL SERVICES LTD` automatically |
| 5 | **Lean-core model shape** (same philosophy as construction) — five models, no speculative tables | Matches ADR-002 — ship what content exists; do not pre-build abandoned shells |

## Model Catalogue

| Model | Purpose | Source of truth |
|---|---|---|
| `FinancialService` | The 9 service lines (loans, agency banking, T-bills, DSE, etc.) | Posters #2 and #3 verbatim |
| `InvestmentOffering` | Productised investment rounds (BFS/IO/2026/01 and /02) | Investment-opportunity posters |
| `Testimonial` | Client / partner quotes | Curated TZ-flavoured placeholders, admin-editable |
| `Certification` | Regulatory registrations / partner bank logos (when client supplies) | Placeholder slot, no fake content |
| `LoanInquiry` | Microfinance lead — personal / SME / group / asset finance | Form on `/financial/loans/apply/` |
| `InvestmentInquiry` | Investment partner lead — capital band, preferred tenure | Form on `/financial/invest/inquire/` |

## URL Map (final state, end of Phase 4)

| Path | View |
|---|---|
| `/financial/` | Home |
| `/financial/about/` | About + values + leadership placeholder |
| `/financial/services/` | All 9 service lines grouped by category |
| `/financial/investments/` | Current + closed offerings list |
| `/financial/investments/<reference_id>/` | Single offering detail with payout calendar |
| `/financial/loans/apply/` | Loan inquiry form |
| `/financial/invest/inquire/` | Investment inquiry form |
| `/financial/contact/` | General contact |

---

## Phase Plan

Each phase = one branch, one PR into `develop`, approved before the next begins.

### Phase 1 — Scaffold (this PR)
- [ ] App created: `apps/financial/` with `FinancialConfig`
- [ ] Added to `INSTALLED_APPS`
- [ ] URL handoff: `path('financial/', include('apps.financial.urls'))` in `config/urls.py`, old Coming Soon route removed from `apps.leads.urls`
- [ ] `apps/financial/urls.py` with `app_name='financial'` and `home` route
- [ ] `base_financial.html` extends `core/base.html`, overrides navbar, navy + gold palette + shared CSS primitives
- [ ] `navbar.html` with two-line BFS wordmark + `Bejundas Group` backlink + primary CTA placeholder
- [ ] `home.html` Phase 1 placeholder: hero, values triad, brief about, regulatory disclaimer
- [ ] Tests: home 200, financial template used, app_theme is navy/gold, `leads:financial` no longer resolves, navbar shows BFS legal entity, disclaimer text present
- [ ] ruff + black + pytest green

### Phase 2 — Models, Admin, Migrations
- [ ] `models.py`: `FinancialService`, `InvestmentOffering`, `Testimonial`, `Certification`, `LoanInquiry`, `InvestmentInquiry` — all inherit `BaseModel`
- [ ] Choices: service categories (loans / investments / agency / securities / auto), offering status (upcoming / open / closed), loan purpose (personal / SME / group / asset), inquiry status workflows (separate pipelines for loans vs investments)
- [ ] Migration `0001_initial`
- [ ] `admin.py`: Unfold `ModelAdmin` for each — list display with thumbnails, status pills, bulk actions on the two inquiry models (mark_reviewed, mark_contacted, etc.)
- [ ] Sidebar config in `config/settings/base.py`: "Financial" collapsible group with 6 entries
- [ ] Tests for `__str__`, defaults, slug auto-fill, choices, status transitions

### Phase 3 — Inner Pages
- [ ] Views: About, Services, Investments list (open/upcoming/closed), Investment detail, Contact
- [ ] Templates: 5 pages built from `demo-insurance` markup, re-skinned to navy + gold
- [ ] Sector / category filter chips on services + investments lists
- [ ] Inner-page hero treatment matching construction's `c-page-hero` pattern
- [ ] Sitemap entries (static pages + dynamic offering detail URLs)
- [ ] Tests: each page 200, correct template, filters narrow correctly, unknown-category falls back

### Phase 4 — Lead Forms (Loan + Investment)
- [ ] `LoanForm` (ModelForm of `LoanInquiry`) — 8 fields, validation including phone format, amount > 0, scope length minimum
- [ ] `InvestmentForm` (ModelForm of `InvestmentInquiry`) — 7 fields, capital_band choices matching offering minimums
- [ ] `LoanApplyView` + `InvestmentInquireView` (FormView subclasses)
- [ ] Email notifications via `EmailMultiAlternatives` (text + branded HTML) to `LEADS_EMAIL` env var
- [ ] Templates: `loan_apply.html`, `investment_inquire.html`, both with 3-section layouts (Personal / Need / Notes)
- [ ] Email HTML templates: `templates/emails/loan_inquiry_notification.{txt,html}` + `investment_inquiry_notification.{txt,html}`
- [ ] Admin: bulk actions (mark_reviewed / mark_contacted / mark_committed/mark_disbursed / mark_lost etc.) per inquiry model
- [ ] Tests: form validation (valid / invalid / each required field), view POST sends email and creates row, admin actions update status

### Phase 5 — Content Seed + Polish + Reports
- [ ] Migration `0002_seed_curated_content.py` (RunPython, idempotent via `update_or_create`):
  - 9 `FinancialService` rows lifted from poster service list
  - 2 `InvestmentOffering` rows: BFS/IO/2026/01 (1yr, 16.5%, TZS 250k min) and BFS/IO/2026/02 (2yr, 18.0%, TZS 250k min) with their dates
  - 4 `Testimonial` rows (curated, TZ-flavoured, admin-editable)
  - Empty `Certification` table — fill when client supplies regulator info
- [ ] Regulatory disclaimer in every page footer + dedicated `disclaimer.html` partial
- [ ] Mobile audit on all 8 pages
- [ ] SEO meta tags + Open Graph images per page
- [ ] `docs/client/financial-vertical-report.html` + `docs/technical/financial-vertical-report.html` matching construction report template, navy/gold theme

---

## Deployment Plan

Per the project's CI/CD: merge `develop` → `main` triggers webhook → migrate runs automatically (including seed migration 0002). No separate seed command needed on cPanel.

After merge:
1. `touch tmp/restart.txt` to recycle Passenger (handled by `scripts/deploy.sh`)
2. Verify: `/financial/` loads, `/admin/` shows the Financial group with 6 entries
3. Test one loan submission + one investment submission end-to-end
4. Re-submit `sitemap.xml` to Google Search Console (8 new financial URLs + 2 offering detail URLs)

---

## Non-Goals (explicit out-of-scope)

| Out of scope | Why |
|---|---|
| End-user accounts / login | No verified requirement; deferred until a vertical actually needs them (ADR-004) |
| Payment integration | Inquiries are leads, not transactions. Money movement happens off-platform (existing client process) |
| KYC document upload | File uploads on a public form for a financial service is a compliance liability. Move to a post-contact stage |
| Live investment performance dashboard | No data source; would be marketing fiction |
| Multi-language toggle (EN/SW) | Use bilingual phrases where natural (tagline, values) but avoid the engineering cost of a translation layer at MVP |
| Loan calculator | Indicative rates only; a calculator implies rates that aren't yet contractually committed |

---

## Brand Assets Status

| Asset | Status | Action |
|---|---|---|
| Parent Bejundas wordmark (SVG) | ✓ available in `Bejundas Logos/brand/` | Wire into `static/images/brand/` in a separate small PR (not blocking Phase 1) |
| Financial-specific logo | Not separately produced — uses parent wordmark + "FINANCIAL SERVICES LTD" line | Render text-only treatment in navbar |
| Office / team photos | Not supplied | Use Viora `demo-insurance` stock + ask client later |
| Regulator badges | Not supplied | Leave `Certification` table empty — do not fabricate |

---

## Stacked PR Map

```
fix/per-vertical-legal-names                ← MERGED (PR #48)
  └─ feature/financial-phase-1-scaffold     ← this PR
       └─ feature/financial-phase-2-models
            └─ feature/financial-phase-3-pages
                 └─ feature/financial-phase-4-forms
                      └─ feature/financial-phase-5-seed-and-polish
                           └─ MERGE to main → production deploy
```
