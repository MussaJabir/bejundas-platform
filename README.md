# Bejundas Platform

Multi-subdomain Django web platform for Bejundas Group of Companies.

One Django project, one Passenger app, one deploy. Subdomains routed via `django-hosts`.

| Subdomain | Status | Description |
|---|---|---|
| `bejundas.co.tz` | Live (MVP) | Parent landing site |
| `financial.bejundas.co.tz` | Coming Soon | Financial Services |
| `construction.bejundas.co.tz` | Coming Soon | Construction & Engineering |
| `energies.bejundas.co.tz` | Coming Soon | Energies & Gas |
| `farming.bejundas.co.tz` | Coming Soon | Farming |
| `investments.bejundas.co.tz` | Coming Soon | Investments & Hospitality |
| `technologies.bejundas.co.tz` | 301 redirect | Redirects to [bjptechnologies.co.tz](https://bjptechnologies.co.tz) |

---

## Stack

- Django 5.x LTS, Python 3.11
- MySQL 8 / MariaDB
- `django-hosts` (subdomain routing)
- `django-unfold` (admin)
- `django-environ` (env var loading)
- WhiteNoise (static files)
- cPanel + Phusion Passenger (hosting)
- GitHub Actions (CI), GitHub Webhooks (deploy)

---

## Quick start (local development)

### Prerequisites

- Python 3.11
- MySQL 8 or MariaDB running locally
- Git

### Setup

```bash
git clone https://github.com/MussaJabir/bejundas-platform.git
cd bejundas-platform

python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt -r requirements-dev.txt

cp .env.example .env
# Edit .env with your local DB credentials and SECRET_KEY

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Subdomain routing in development

Add to `/etc/hosts`:

```
127.0.0.1   bejundas.local
127.0.0.1   financial.bejundas.local
127.0.0.1   construction.bejundas.local
127.0.0.1   energies.bejundas.local
127.0.0.1   farming.bejundas.local
127.0.0.1   investments.bejundas.local
127.0.0.1   technologies.bejundas.local
```

Visit `http://bejundas.local:8000` (hub) and `http://financial.bejundas.local:8000` (Coming Soon themed for financial).

---

## Run tests

```bash
pytest
ruff check .
black --check .
```

---

## Project documentation

- [CLAUDE.md](CLAUDE.md) — master spec for AI assistants and developers
- [SESSION_LOG.md](SESSION_LOG.md) — append-only progress log
- [CONTRIBUTING.md](CONTRIBUTING.md) — branching workflow, commit style
- [docs/deployment.md](docs/deployment.md) — cPanel + webhook deploy
- [docs/branching.md](docs/branching.md) — git workflow
- [docs/database.md](docs/database.md) — MySQL setup
- [docs/adding-a-vertical.md](docs/adding-a-vertical.md) — playbook for adding new vertical apps
- [CHANGELOG.md](CHANGELOG.md) — release notes

---

## License

Proprietary. All rights reserved. See [LICENSE](LICENSE).

---

## Contact

For project-related issues, open an issue in this repo.
For business enquiries: info@bejundas.co.tz
