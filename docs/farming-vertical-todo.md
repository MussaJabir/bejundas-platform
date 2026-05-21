# Farming Vertical — Implementation Plan

> Build the `bejundas.co.tz/farming/` vertical for **BEJUNDAS FARMING LTD**.
> Replaces the current `apps.leads.coming_soon` route at `/farming/`.
> Stacked PRs into `develop`. Each phase waits for explicit approval before the next starts.
>
> Same workflow as construction (PRs #42-#46) and financial (PRs #49-#53).

---

## Source material status

Sparse. Hearsay-only at plan time:
- Legal entity: **BEJUNDAS FARMING LTD**
- Activities: farms (crops) + poultry + "other activities"
- No posters, no photos, no licence info, no concrete product list

→ Curated TZ-flavoured content based on common mid-market agribusiness in Tanzania. Admin-editable row-by-row when real client info arrives. Same posture as construction (which also had no real client content at build time).

---

## Scope — Proposed defaults (confirm at Phase 1 kickoff)

| # | Decision | Rationale |
|---|---|---|
| 1 | **Brand values triad: Asili · Ubora · Uaminifu** (Natural · Quality · Trust) | Farming-appropriate. Trust pillar mirrors financial's *Uaminifu*. Easy to swap to a client-supplied triad. |
| 2 | **Both wholesale and retail** distinguished by `inquiry_type` in a single OrderInquiry form | The audiences are different but the funnel mechanics are the same (buyer reaches out → we respond with availability + pricing → fulfilment). Two separate forms would be over-engineering — different shape from financial's loan vs investment (those had fundamentally different workflows). |
| 3 | **2 placeholder Farm rows** (Mbeya Highland Farm / Coast Region Poultry Farm) | Tangible enough to render a Farms page. Easy to delete if client only has one site. |
| 4 | **No prices on products** — "Inquire for current pricing" CTA instead | Commodity prices fluctuate. Locking a number in HTML invites disputes. Admin can add a price field later if they want. |
| 5 | **Seed mix (9 products)** — 5 crops + 3 poultry + 1 processed: maize · sunflower · beans · vegetables · fruits · layer eggs · broilers · local kienyeji chickens · sunflower oil | Coherent mid-market TZ agribusiness profile, all 3 categories used. |
| 6 | **OrderInquiry workflow (6 states)** — `new → contacted → quoted → fulfilled → declined → closed` | Mirrors construction's RFP shape — fits "lead → response → conversion → completion" flow naturally. |

---

## Model Catalogue (5 models — lean core)

| Model | Purpose | Notable fields |
|---|---|---|
| `FarmingProduct` | What they sell | name, slug, category (crops / poultry / processed), summary, description, unit (kg/dozen/each/litre), image, is_active, is_featured, order |
| `Farm` | Physical farm locations | name, slug, region, size_hectares, primary_activity, description, cover_image, order |
| `Testimonial` | Customer / partner quotes | Same shape as construction/financial (with `__test__ = False`) |
| `Certification` | TBS / organic / food-safety registrations | Empty by default — fill when client supplies |
| `OrderInquiry` | Single lead funnel | full_name, organisation (opt), email, phone, inquiry_type (wholesale / retail / partnership), products_of_interest (text — not M2M, simpler), quantity (text), frequency (one_off / monthly / seasonal), delivery_location (region), notes, preferred_contact, status (6 states), internal_notes |

---

## URL Map (final state, end of Phase 4)

| Path | View |
|---|---|
| `/farming/` | Home |
| `/farming/about/` | About + values + farming philosophy + certifications |
| `/farming/products/` | Products list with category filter (crops / poultry / processed) |
| `/farming/farms/` | Our farms (location cards) |
| `/farming/order/` | OrderInquiry form |
| `/farming/contact/` | General contact |

---

## Brand & Palette

| | |
|---|---|
| Primary | `#2d5a27` — forest green (already in `VerticalPlaceholder` + `app_theme` context processor) |
| Accent | `#8bc34a` — lime green |
| Soft   | `#f1f8e9` — pale leaf (derived) |
| Viora demo (home) | `demo-agriculturefarming` |
| Viora demos (inner pages) | port from `demo-corporate` + `demo-gardenlandscaping` for visuals (per CLAUDE.md §14) |
| Legal name | `BEJUNDAS FARMING LTD` — to be added to `app_theme.legal_name` in Phase 1 |

---

## Phase Plan

Each phase = one branch, one PR into `develop`, approved before the next begins.

### Phase 1 — Scaffold + green palette + home placeholder
- [ ] `apps.farming` app created, registered in `INSTALLED_APPS`
- [ ] URL handoff: `path('farming/', include('apps.farming.urls'))` in `config/urls.py`, old Coming Soon route removed from `apps.leads.urls`
- [ ] `apps/farming/urls.py` with `app_name='farming'` and `home` route
- [ ] `base_farming.html` extends `core/base.html`, overrides navbar, forest-green + lime palette + shared CSS primitives
- [ ] `navbar.html` with two-line `BEJUNDAS FARMING / LTD` wordmark + Bejundas Group backlink
- [ ] `home.html` Phase 1 placeholder: hero, Asili / Ubora / Uaminifu values strip, brief about, WhatsApp CTA
- [ ] Add `farming` legal_name to `app_theme` in context_processor
- [ ] Tests: home 200, farming template used, app_theme is forest/lime, `leads:farming` no longer resolves, navbar shows legal entity, values present
- [ ] ruff + black + pytest green

### Phase 2 — Models, Admin, Migrations
- [ ] `models.py`: `FarmingProduct`, `Farm`, `Testimonial`, `Certification`, `OrderInquiry` — all inherit `BaseModel`
- [ ] Choices: product category (crops / poultry / processed), inquiry type (wholesale / retail / partnership), frequency (one_off / monthly / seasonal), inquiry status (6 states)
- [ ] Migration `0001_initial`
- [ ] `admin.py`: Unfold `ModelAdmin` for each with thumbnails, status pills, category pills, bulk actions on OrderInquiry (`mark_contacted`, `mark_quoted`, `mark_fulfilled`, `mark_declined`, `mark_closed`)
- [ ] `get_absolute_url()` on `Farm` (for admin View-on-site)
- [ ] Sidebar config: "Farming" collapsible group with 5 entries
- [ ] Tests for `__str__`, defaults, slug auto-fill, choices

### Phase 3 — Inner Pages
- [ ] Views: About, Products (with category filter), Farms list, Contact
- [ ] Templates: re-skinned from `demo-agriculturefarming` markup, forest-green palette
- [ ] Category filter chips on products page
- [ ] Inner-page hero treatment matching financial's `f-page-hero` pattern (now `g-page-hero` for farming)
- [ ] Home rewired to pull featured products + featured farms from Phase 2 models
- [ ] Dedicated sitemap module + register in `config/urls.py`
- [ ] Tests: each page 200, correct template, filter narrows correctly, unknown-category falls back

### Phase 4 — OrderInquiry Form
- [ ] `OrderInquiryForm` (ModelForm) with phone validation (≥9 digits) and `inquiry_type` choice
- [ ] `OrderInquireView` (GET/POST) with `_validate_phone` shared helper
- [ ] Template: `order.html` with 3-section layout (Buyer / Order Details / Notes)
- [ ] Branded email templates: `templates/emails/order_inquiry_notification.{txt,html}` — green/lime header, sections for buyer + order, "Review in Admin" CTA
- [ ] Email send wrapped in try/except (lesson learned from PR #55 — best-effort)
- [ ] Sitemap extended with `/farming/order/`
- [ ] Tests: form validation (valid/invalid), view POST creates row + sends email, email failure shows success not 500

### Phase 5 — Content Seed + Polish + Reports
- [ ] Migration `0002_seed_curated_content.py` (RunPython, idempotent via `update_or_create`):
  - **9 `FarmingProduct` rows** — 5 crops + 3 poultry + 1 processed
  - **2 `Farm` rows** — Mbeya Highland Farm (crops) + Coast Region Poultry Farm (layers/broilers)
  - **4 `Testimonial` rows** — wholesale buyer, retail customer, contract farmer, local restaurant
  - Empty `Certification` table — fill when client supplies
- [ ] Disclaimer partial `_disclaimer.html` with 3 variants (default / products / order) — covers food safety / quality / "subject to availability" notes
- [ ] Organization JSON-LD on home page (Schema.org `LocalBusiness` or `Farm` type)
- [ ] Mobile audit on all 6 pages
- [ ] `docs/client/farming-vertical-report.html` + `docs/technical/farming-vertical-report.html` matching financial/construction report template, forest-green / lime theme

---

## Deployment Plan

Per the project's CI/CD: merge `develop` → `main` triggers webhook → `migrate` runs automatically (including seed migration 0002). No separate seed command on cPanel.

After merge:
1. `touch tmp/restart.txt` to recycle Passenger
2. Verify: `/farming/` loads, `/admin/` shows the Farming group with 5 entries
3. Test one order submission end-to-end (form → row → email)
4. Re-submit `sitemap.xml` to Google Search Console (6 farming pages)

---

## Non-Goals (explicit out-of-scope)

| Out of scope | Why |
|---|---|
| E-commerce checkout / payment | Inquiries are leads, not orders. Money movement happens off-platform (existing client process — phone / bank transfer / M-Pesa) |
| Live inventory / stock counts | Would create a maintenance burden. "Inquire for availability" is honest and saves the admin from constant updates |
| Online customer accounts | No verified requirement; ADR-004 — deferred until a vertical actually needs accounts |
| Pricing displayed on the site | Commodity prices fluctuate weekly. Inquiry-first lets the business negotiate by volume / season / relationship |
| Multi-language toggle (EN/SW) | Use bilingual phrases where natural (tagline, values) but avoid the engineering cost of a translation layer at MVP — same as financial |
| Crop calendar / planting schedule visualisation | No data source; would be marketing fiction |

---

## Stacked PR Map

```
docs/farming-vertical-plan                  ← this PR (the plan)
   ↓
feature/farming-phase-1-scaffold            ← Phase 1
   └─ feature/farming-phase-2-models
        └─ feature/farming-phase-3-pages
             └─ feature/farming-phase-4-order
                  └─ feature/farming-phase-5-seed-and-polish
                       └─ MERGE to main → production deploy
```

---

## Open questions to confirm at Phase 1 kickoff

If any of the 6 scope decisions in §"Scope — Proposed defaults" need to change before we cut Phase 1, flag them then. Otherwise we proceed with the defaults above.
