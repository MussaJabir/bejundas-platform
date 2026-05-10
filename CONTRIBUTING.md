# Contributing to Bejundas Platform

This is a client project. External contributions are not accepted at this time. This document is for the internal development team.

---

## Workflow

### 1. Branch from `develop`

```bash
git checkout develop
git pull
git checkout -b <type>/<short-description>
```

Branch types:

| Prefix | Use for |
|---|---|
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `hotfix/` | Emergency production fixes (branch from `main` instead of `develop`) |
| `chore/` | Dependencies, configs, CI, non-code |
| `docs/` | Documentation only |

Branch names are lowercase, hyphen-separated.

Examples:
```
feature/hub-contact-form
fix/coming-soon-host-fallback
chore/upgrade-django-5.1.4
docs/deployment-guide
hotfix/passenger-restart-loop
```

### 2. Commit using Conventional Commits

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
test(hub): add tests for ContactForm validation
ci(deploy): add MySQL service container to test workflow
```

### 3. Run checks before pushing

```bash
ruff check .
black --check .
pytest
```

If any of these fail, fix before pushing.

### 4. Open a Pull Request

- Target branch: `develop` (always)
- Use the PR template (auto-loaded from `.github/PULL_REQUEST_TEMPLATE.md`)
- Link related issues
- Assign yourself
- Wait for CI to pass before requesting review

### 5. Merge

- Squash and merge from `feature/*` to `develop`
- Merge commit (no squash) from `develop` to `main`
- Delete the branch after merge

### 6. Update SESSION_LOG.md

Append a new session entry at the end of each working session. Never delete previous entries. Commit the log update with the same PR or as a separate `docs/session-N` PR.

---

## What CI checks

- `ruff check .` — linting
- `black --check .` — formatting
- `pytest` — full test suite against MySQL 8 service container

CI must pass before any merge.

---

## What goes where

| Concern | Location |
|---|---|
| Project settings | `config/settings/` |
| Subdomain routing | `config/hosts.py` |
| Root URL conf | `config/urls.py` |
| Shared base templates, BaseModel, SiteSettings | `apps/core/` |
| Hub site (bejundas.co.tz) | `apps/hub/` |
| Coming Soon + Lead model | `apps/leads/` |
| Future vertical apps | `apps/<vertical>/` (one per vertical) |
| Static assets | `static/` |
| Global templates (404, 500, base) | `templates/` |
| User uploads | `public/media/` (gitignored) |
| collectstatic output | `public/static/` (gitignored) |
| Documentation | `docs/` |
| Deploy scripts | `scripts/` |
| GitHub Actions + templates | `.github/` |

---

## Code style

- Run `ruff check .` and `black --check .` before committing
- Line length: 100 (configured in `pyproject.toml`)
- All Django models inherit from `apps.core.models.BaseModel`
- All Django templates extend `core/base.html`
- All URL references use `{% url 'appname:action' %}` — never hardcode paths
- All env var access goes through `django-environ` in `config/settings/base.py`

For full coding conventions see [CLAUDE.md §15](CLAUDE.md).

---

## Adding a new vertical app

See [docs/adding-a-vertical.md](docs/adding-a-vertical.md) and [CLAUDE.md §13](CLAUDE.md).

---

## Reporting security issues

See [SECURITY.md](SECURITY.md). Do not open public issues for security vulnerabilities.
