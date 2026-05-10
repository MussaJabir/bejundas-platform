# Git Branching Workflow

This document is the operational guide for git workflow in `bejundas-platform`.

---

## Branch hierarchy

```
main           Production. Protected. Webhook deploys from here.
  ^
  |  PR review + CI green
  |
develop        Integration. Protected from direct push.
  ^
  |  PR review + CI green
  |
feature/*      Short-lived. Branched from develop. Merged back to develop.
fix/*
chore/*
docs/*
hotfix/*       Emergency. Branched from main. Merged to main AND develop.
```

---

## Branch naming

Lowercase, hyphen-separated, prefixed with type.

| Prefix | Use for | Examples |
|---|---|---|
| `feature/` | New functionality | `feature/hub-contact-form`, `feature/vertical-financial` |
| `fix/` | Bug fixes | `fix/coming-soon-host-fallback`, `fix/email-utf8-encoding` |
| `hotfix/` | Emergency production fixes | `hotfix/passenger-restart-loop`, `hotfix/csrf-token-mismatch` |
| `chore/` | Deps, configs, CI | `chore/upgrade-django-5.1.4`, `chore/add-pre-commit-hook` |
| `docs/` | Documentation only | `docs/deployment-guide`, `docs/session-3` |

Bad names (avoid):
- `mybranch` (no type prefix)
- `Feature/HubContactForm` (camelCase, capitals)
- `feature/contact_form` (underscores)

---

## Workflow per task

### Standard feature/fix/chore/docs

1. Sync local `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   ```

2. Create branch:
   ```bash
   git checkout -b feature/hub-contact-form
   ```

3. Work, commit (Conventional Commits — see below):
   ```bash
   git add apps/hub/forms.py apps/hub/views.py apps/hub/templates/hub/contact.html
   git commit -m "feat(hub): add contact form with email notification"
   ```

4. Run local checks:
   ```bash
   ruff check .
   black --check .
   pytest
   ```

5. Push and open PR to `develop`:
   ```bash
   git push -u origin feature/hub-contact-form
   gh pr create --base develop --fill
   ```

6. Wait for CI to pass.
7. Get review, address feedback.
8. Squash and merge.
9. Delete the feature branch (GitHub UI or `git push origin --delete feature/hub-contact-form`).

### Hotfix (production is broken)

1. Sync local `main`:
   ```bash
   git checkout main
   git pull origin main
   ```

2. Create hotfix:
   ```bash
   git checkout -b hotfix/passenger-restart-loop
   ```

3. Fix, commit, push, open PR to `main` (not `develop`).
4. Get fast review, merge to `main`. Webhook deploys automatically.
5. **Then** also merge `main` back into `develop` to keep them in sync:
   ```bash
   git checkout develop
   git pull origin develop
   git merge main
   git push origin develop
   ```

### Releasing develop to production

When `develop` is stable and ready to ship:

1. Open PR from `develop` to `main`
2. Use a merge commit (no squash) to preserve history of features
3. Title: `chore(release): merge develop -> main (YYYY-MM-DD)`
4. Get review
5. Merge. Webhook fires. Site updates.
6. Append SESSION_LOG.md entry.

---

## Conventional Commits

```
type(scope): short description

[optional body explaining why]

[optional footer for breaking changes or issue references]
```

### Types

| Type | When to use |
|---|---|
| `feat` | New feature visible to users |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, whitespace (no code change) |
| `refactor` | Code change that's neither feat nor fix |
| `test` | Adding or updating tests |
| `chore` | Deps, build, configs, anything else |
| `ci` | CI/CD changes |

### Scope

Use the app or area being touched: `hub`, `leads`, `core`, `deps`, `deploy`, `admin`, `hosts`.

### Examples

Good:
```
feat(hub): add contact form with email notification
fix(leads): correct VerticalPlaceholder fallback when host unknown
chore(deps): pin Django to 5.1.4
test(hub): cover ContactForm validation paths
ci(deploy): add MySQL service container to test workflow
docs(deploy): document webhook secret rotation procedure
refactor(core): extract company_info context processor into separate module
```

Bad (avoid):
```
update files
fix bug
WIP
asdf
fixed the thing
```

### Breaking changes

```
feat(hub)!: rename Service.icon to Service.icon_class

BREAKING CHANGE: existing data needs migration. Run:
python manage.py migrate hub 0007
```

---

## PR requirements

- Title follows Conventional Commits format
- Description fills out PR template:
  - Summary (1-3 bullets)
  - Test plan
  - Screenshots if UI changes
- CI green
- At least one approving review (self-approve allowed for solo dev mode but should be flagged in commit body)
- Linked to an issue if applicable

---

## Branch protection (configure in GitHub Settings > Branches)

### `main`
- Require pull request before merging
- Require status checks (CI) to pass
- Require branches to be up to date before merging
- Do not allow force pushes
- Do not allow deletions

### `develop`
- Require pull request before merging
- Require status checks (CI) to pass
- Allow force pushes: false (rebase via PR if needed)
- Do not allow deletions

---

## What NOT to do

- Don't `git push --force` to `main` or `develop`
- Don't merge a PR with failing CI
- Don't commit directly to `main` or `develop`
- Don't delete the feature branch before the PR is merged
- Don't leave WIP commits in a PR — squash them before requesting review (or rely on squash-merge)
- Don't use `git rebase` on a branch that's already pushed and shared
- Don't include unrelated changes in a single PR — split them
