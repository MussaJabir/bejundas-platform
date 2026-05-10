# Deployment Guide — cPanel + Phusion Passenger + GitHub Webhook

This document is the operational guide for deploying `bejundas-platform` to cPanel.

---

## Architecture

```
Developer pushes to main
        |
        v
GitHub fires webhook -> https://bejundas.co.tz/deploy/webhook/
        |
        v
apps.core.webhook validates HMAC signature
        |
        v
Spawns detached scripts/deploy.sh (start_new_session=True)
        |
        v
git pull -> pip install -> migrate -> collectstatic -> touch tmp/restart.txt
        |
        v
Passenger restarts the Python App, serves new code
```

This pattern was chosen because the hosting provider blocks SSH (port 22) and the cPanel UAPI (port 2083) externally. See [bjp-technologies-web Session 13](https://github.com/MussaJabir/bjp-technologies-web/blob/main/SESSION_LOG.md) for the lessons learned.

---

## One-time cPanel setup

### 1. MySQL database

cPanel home > **MySQL Databases**

- Create database: `bejundas_db` (cPanel may prefix the username, e.g. `bejundas_bejundas_db`)
- Create user: `bejundas_dbuser`
- Set a strong password (save in `.env` on server)
- Add user to database with **ALL PRIVILEGES**
- Verify charset is `utf8mb4` and collation is `utf8mb4_unicode_ci`

### 2. Subdomains

cPanel home > **Domains** > **Create A New Domain**

For each of the following 6 subdomains:
- `financial.bejundas.co.tz`
- `construction.bejundas.co.tz`
- `energies.bejundas.co.tz`
- `farming.bejundas.co.tz`
- `investments.bejundas.co.tz`
- `technologies.bejundas.co.tz`

In the create form:
- Domain: enter the subdomain
- Toggle **"Share document root with bejundas.co.tz"** to **ON**

This routes all subdomain requests through the same Passenger app as the main domain.

### 3. Python App

cPanel home > **Setup Python App** > **Create Application**

- Python version: **3.11**
- Application root: `bejundas_platform` (cPanel will create `/home/bejundas/bejundas_platform/`)
- Application URL: `bejundas.co.tz`
- Application startup file: `passenger_wsgi.py`
- Application Entry point: `application`
- Passenger log file: `/home/bejundas/logs/passenger.log`

After creation, cPanel gives a `source virtualenv/...` command. Copy it — you will use it in the deploy script.

### 4. SSL/TLS

cPanel home > **SSL/TLS Status** > select all 7 hostnames > **Run AutoSSL**

Verify each hostname gets a valid certificate. If AutoSSL fails for a subdomain, ensure DNS is pointing correctly.

Optional but recommended: put **Cloudflare** in front for caching, free wildcard SSL fallback, and DDoS protection.

### 5. Environment file on server

Via cPanel **File Manager** or **SSH** (if available), create `/home/bejundas/bejundas_platform/.env` with values from `.env.example`. Critical:

- `DEBUG=False`
- `SECRET_KEY=<generate a fresh 50-char random string>`
- `ALLOWED_HOSTS=bejundas.co.tz,www.bejundas.co.tz,financial.bejundas.co.tz,construction.bejundas.co.tz,energies.bejundas.co.tz,farming.bejundas.co.tz,investments.bejundas.co.tz,technologies.bejundas.co.tz`
- `PARENT_HOST=bejundas.co.tz`
- `DB_NAME`, `DB_USER`, `DB_PASS`, `DB_HOST=localhost`, `DB_PORT=3306`
- `EMAIL_*` settings
- `GITHUB_WEBHOOK_SECRET=<generate a fresh 64-char random string>` — keep a copy for GitHub webhook config

### 6. Initial deploy

Through cPanel **Git Version Control**:
- Create new repo
- Clone URL: `https://github.com/MussaJabir/bejundas-platform.git`
- Repository path: `/home/bejundas/bejundas_platform`
- Branch: `main`

Then run via cPanel Terminal (if available) or via the Python App's "Run pip install" feature:
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
touch tmp/restart.txt
```

Verify the site loads at `https://bejundas.co.tz`.

### 7. Configure GitHub webhook

GitHub repo > **Settings** > **Webhooks** > **Add webhook**

- Payload URL: `https://bejundas.co.tz/deploy/webhook/`
- Content type: `application/json`
- Secret: paste the same value as `GITHUB_WEBHOOK_SECRET` from server `.env`
- Events: **Just the push event**
- Active: checked

Test by pushing a small change to `main`. Verify:
- Webhook delivery shows `200 OK` in GitHub's webhook log
- `/tmp/bjp_deploy.log` on the server shows the deploy ran
- New code is live

---

## Deploy on every change

Once setup is complete:

1. Open PR to `develop`, get review, merge
2. Open PR from `develop` to `main`, get review, merge
3. GitHub fires webhook automatically
4. Site updates within 30-60 seconds
5. Watch `/tmp/bjp_deploy.log` to confirm

No manual SSH, no FTP, no cPanel clicks.

---

## Manual deploy fallback

If the webhook ever fails:

1. SSH or cPanel Terminal into the server
2. `cd /home/bejundas/bejundas_platform`
3. `bash scripts/deploy.sh`

Or step-by-step:
```bash
cd /home/bejundas/bejundas_platform
git pull origin main
source /home/bejundas/virtualenv/bejundas_platform/3.11/bin/activate
pip install -r requirements.txt --quiet
python manage.py migrate --no-input
python manage.py collectstatic --no-input
touch tmp/restart.txt
```

---

## Rollback

1. Via GitHub: revert the offending commit on `main` and push
2. Webhook fires, deploys the reverted state

If the webhook itself is broken: SSH and `git reset --hard <previous-good-commit>`, then run the manual deploy steps above.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| 500 error after deploy | Migration failed | Check `/tmp/bjp_deploy.log`; run migrate manually |
| Static files missing | `collectstatic` failed | Check disk space; run manually |
| Site doesn't restart | `tmp/restart.txt` not touched | Run `touch tmp/restart.txt` manually |
| Webhook returns 401 | HMAC mismatch | Confirm `GITHUB_WEBHOOK_SECRET` matches in both places |
| Webhook returns 200 but no deploy | Detached process died silently | Check `/tmp/bjp_deploy.log` and `passenger.log` |
| Subdomain shows main site instead of Coming Soon | Document root not shared | Re-create subdomain with "Share document root" ON |
| `ALLOWED_HOSTS` error | Subdomain not in env var | Add to `.env` `ALLOWED_HOSTS`, redeploy |

---

## Logs

| Log | Path | What it shows |
|---|---|---|
| Deploy log | `/tmp/bjp_deploy.log` | Output of `scripts/deploy.sh` |
| Passenger log | `/home/bejundas/logs/passenger.log` | Python app errors, restarts |
| Django log | `/home/bejundas/bejundas_platform/logs/django.log` | Application errors (if configured) |
| Apache error log | cPanel > **Errors** | Web server errors |
