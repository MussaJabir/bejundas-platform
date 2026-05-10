# SESSION_LOG.md — Bejundas Platform

> This file is updated at the end of every working session.
> It is the single source of truth for project progress, decisions, and context.
> Never delete entries. Always append new entries at the bottom.
> Committed to git at the end of every session.

---

## Project Summary

**Repo:** [bejundas-platform](https://github.com/MussaJabir/bejundas-platform)
**Domain:** bejundas.co.tz (primary) + 6 subdomains
**Stack:** Django 5.x LTS + MySQL + cPanel + Phusion Passenger + GitHub Actions
**Current Phase:** Phase 0 — Infrastructure & cPanel setup
**Started:** 2026-05-10

## Phase Progress

| Phase | Name | Status |
|---|---|---|
| Phase 0 | Infrastructure & cPanel setup | In Progress |
| Phase 1 | Repo scaffold & Django bootstrap | TODO |
| Phase 2 | Hub site (home, about, services, news, team, contact) | TODO |
| Phase 3 | Coming Soon system (5 placeholder subdomains) | TODO |
| Phase 4 | Webhook deploy + CI + first production push | TODO |
| Phase 5 | Polish, mobile, SEO, soft launch | TODO |

---

## Session 0 — 2026-05-10 EAT

**Goal:** Project planning. Lock architecture, scope, stack, and deliverables before writing any code.
**Branch:** N/A (pre-scaffold session)
**Status:** Complete

### What Was Done

- Reviewed the original `Bejundas Website/CLAUDE.md` proposal (monorepo, 7 apps, custom user model with `app_access`, 7 themed AdminSites, django-ckeditor, PostgreSQL/SQLite split)
- Reviewed the live `bjp-technologies-web` repo: branching workflow, GitHub Actions, webhook deploy pattern, SiteSettings + proxy admin pattern, SESSION_LOG.md discipline
- Reviewed the Viora HTML5 template folder: 20 demos, only 5 ship full page sets (`demo-corporate`, `demo-agency`, `demo-medical`, `demo-spasalon`, `demo-insurance`)
- Confirmed cPanel hosting capabilities for `bejundas.co.tz`:
  - Domains UI accepts wildcard subdomain creation (`*` accepted)
  - "Share document root with bejundas.co.tz" toggle exists — multiple subdomains can share one Passenger app
  - Setup Python App allows picking the Application URL from the domain dropdown
  - One Python App can serve all subdomains via shared document root
- Resolved 4 hard contradictions between the original CLAUDE.md and reality:
  1. Monorepo vs 6 separate repos — picked monorepo
  2. Technologies app conflict (live `bjptechnologies.co.tz` exists in separate repo) — keep separate, drop from monorepo, 301 redirect from `technologies.bejundas.co.tz`
  3. Database mismatch (Postgres/SQLite proposed, but cPanel only supports MySQL) — picked MySQL for both dev and prod
  4. Django version conflict (5.x vs 6.x) — picked 5.x LTS
- Confirmed all 6 verticals are aspirational (no real content yet) — pivoted scope to "hub fully built + 5 verticals as themed Coming Soon pages with lead capture"
- Cut scope from original CLAUDE.md:
  - 7 apps reduced to 3 (`core`, `hub`, `leads`)
  - Custom `BejundasUser` with `app_access` JSONField removed — use `AbstractUser` only
  - 7 `AdminSite` subclasses removed — single Unfold admin with per-app accent
  - django-ckeditor removed (CKEditor 4 EOL) — use Unfold's built-in TinyMCE
  - django-crispy-forms removed — use `django-widget-tweaks` instead
  - python-decouple swapped for `django-environ`
- Created GitHub repo `bejundas-platform` (public) under `MussaJabir/bejundas-platform`
- Cloned empty repo into `/home/j4bir/Dev/BJP/Projects/Web/Bejundas Website/bejundas-platform/`
- Wrote initial doc set: CLAUDE.md (master spec), SESSION_LOG.md (this file), README, CONTRIBUTING, CHANGELOG, SECURITY, docs/, .github/, requirements files, configs
- Documented "Adding a New Vertical" playbook in CLAUDE.md §13 so verticals 2-6 can be added later without re-architecting

### Files Changed

| File | Action | Notes |
|---|---|---|
| CLAUDE.md | Created | 18-section master spec with ADRs, phase plan, vertical playbook |
| SESSION_LOG.md | Created | This file |
| README.md | Created | Public-facing project description |
| CONTRIBUTING.md | Created | Branching workflow, commit style |
| CHANGELOG.md | Created | Keep a Changelog format, [Unreleased] |
| SECURITY.md | Created | Vulnerability disclosure |
| LICENSE | Created | Proprietary, all rights reserved |
| docs/deployment.md | Created | cPanel + webhook deploy guide |
| docs/branching.md | Created | Git workflow details |
| docs/database.md | Created | MySQL setup, migration rules |
| docs/adding-a-vertical.md | Created | Long-form playbook |
| .github/workflows/deploy.yml | Created | Tests-only CI (deploy is webhook-driven) |
| .github/PULL_REQUEST_TEMPLATE.md | Created | PR checklist |
| .github/ISSUE_TEMPLATE/bug_report.md | Created | |
| .github/ISSUE_TEMPLATE/feature_request.md | Created | |
| .gitignore | Created | Python + Django + cPanel + IDE |
| .env.example | Created | Template for .env |
| requirements.txt | Created | Pinned production deps |
| requirements-dev.txt | Created | pytest, ruff, black, factory_boy |
| pyproject.toml | Created | ruff + black config |
| pytest.ini | Created | Django test runner config |
| .cpanel.yml | Created | Post-deploy tasks |

### Decisions Made

- **Decision:** Monorepo with `django-hosts`, single Passenger app serving all 7 hostnames via shared document root.
  **Reason:** cPanel's "Share document root" toggle makes this clean. Six separate Passenger apps would mean six virtualenvs, six webhook deploys, six SSL renewals — unmaintainable for a solo developer on shared hosting. Lessons from `bjp-technologies-web` Session 13 confirmed.

- **Decision:** Hub fully built; 5 verticals get themed Coming Soon pages with lead-capture form (`apps.leads`).
  **Reason:** Client confirmed no vertical has real content yet. Building 6 vertical-specific apps with placeholder content creates 6 abandoned shells. Coming Soon + lead capture converts visitors into a queryable lead pipeline, which is more valuable than a fake services page.

- **Decision:** MySQL for both dev and production. No SQLite fallback.
  **Reason:** cPanel only supports MySQL. SQLite-in-dev creates surprises in production (charset, JSONField, case sensitivity). Match production locally.

- **Decision:** Drop the proposed `BejundasUser(AbstractUser)` with `app_access JSONField`.
  **Reason:** YAGNI. Public verticals don't need user accounts at MVP. Admin users use Django Groups for per-app permissions. If end-user accounts are needed later, that vertical adds them.

- **Decision:** One Unfold-themed admin, not 7 `AdminSite` subclasses.
  **Reason:** Custom AdminSite classes break Django's admin URL registry and double maintenance cost. Unfold's existing theming covers per-section branding.

- **Decision:** Carry over from `bjp-technologies-web`: webhook deploy pattern (`apps/core/webhook.py` + `scripts/deploy.sh`), CI workflow (tests-only), branching workflow (main/develop/feature/fix/chore), `BaseModel` (UUID + timestamps), `SiteSettings` singleton + proxy admin pattern, SESSION_LOG.md discipline.
  **Reason:** Already proven in production. Don't re-solve solved problems.

- **Decision:** GitHub repo is public, license is proprietary (all rights reserved).
  **Reason:** Client work. Public for visibility / sharing with client. Proprietary license signals reuse is not permitted.
  **Risk:** Public repo + secrets = permanent leak if `.env` is ever committed. Mitigated by strict `.gitignore` and `.env.example` discipline. Pre-commit hook recommended in Phase 1.

- **Decision:** `technologies.bejundas.co.tz` is a 301 redirect to `bjptechnologies.co.tz`. Not a Django app in this repo.
  **Reason:** The technologies site is already live in `bjp-technologies-web`. Migrating it into this monorepo would lose deploy history and risk breaking a working site for no real benefit.

- **Decision:** Django 5.x LTS, not Django 6.x.
  **Reason:** Stability over newness for client work on cPanel + Passenger. Django 6 is too fresh for Passenger's WSGI quirks.

- **Decision:** Add `LEADS_EMAIL` env var separate from `CONTACT_EMAIL`.
  **Reason:** Hub contact form goes to one inbox; Coming Soon callback leads from 5 different verticals can route to different inboxes (or different folders) for triage.

### Next Session Should

- [ ] Phase 0: User finishes cPanel setup (MySQL DB, 6 subdomains with shared document root, Python App, AutoSSL)
- [ ] Phase 1 begins: Claude scaffolds Django project (`config/`, `apps/core/`, `apps/hub/`, `apps/leads/`, settings split, `manage.py`, `passenger_wsgi.py`)
- [ ] Phase 1: Wire `django-hosts`, Unfold admin, `BaseModel`, `SiteSettings` singleton + proxy admin pattern
- [ ] Phase 1: First green CI run on `develop` branch
- [ ] Confirm `develop` branch protection rules + `main` branch protection rules in GitHub repo settings

---
