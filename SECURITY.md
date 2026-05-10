# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please **do not open a public GitHub issue**.

Instead, send an email to **info@bejundas.co.tz** with:

- A description of the vulnerability
- Steps to reproduce
- The affected URL or endpoint
- Your contact information (optional, for follow-up)

We will acknowledge receipt within 7 days and aim to address valid reports within 30 days.

---

## Scope

In scope:
- `bejundas.co.tz` and all `*.bejundas.co.tz` subdomains served by this codebase
- Code in this repository

Out of scope:
- `bjptechnologies.co.tz` — see the [bjp-technologies-web](https://github.com/MussaJabir/bjp-technologies-web) repository for that site's security policy
- Third-party services (cPanel, Cloudflare, etc.)
- Social engineering, physical security, denial of service

---

## Secrets handling

- The `.env` file is gitignored and **must never** be committed
- This is a **public repository** — any leaked secret in git history is permanently exposed
- If a secret is committed by mistake:
  1. Rotate the secret immediately at its source (database password, SMTP password, GitHub webhook secret, Django `SECRET_KEY`)
  2. Open an issue tagged `security` to track the rotation
  3. Consider using `git filter-repo` to scrub the value from history (note: GitHub caches do not always honor force-pushes; rotation is the only real fix)

---

## Supported versions

Only the `main` branch receives security fixes. There are no released versions to backport to.
