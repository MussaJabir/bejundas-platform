# Bejundas Platform

Django web platform for Bejundas Group of Companies.

One Django project, one Passenger app, one deploy. All verticals live under the single `bejundas.co.tz` host as URL paths (see CLAUDE.md ADR-007).

| URL | Status | Description |
|---|---|---|
| `bejundas.co.tz` | Live (MVP) | Parent landing site |
| `bejundas.co.tz/financial/` | Coming Soon | Financial Services |
| `bejundas.co.tz/construction/` | Coming Soon | Construction & Engineering |
| `bejundas.co.tz/energies/` | Coming Soon | Energies & Gas |
| `bejundas.co.tz/farming/` | Coming Soon | Farming |
| `bejundas.co.tz/investments/` | Coming Soon | Investments & Hospitality |
| `bejundas.co.tz/technologies/` | 301 redirect | Redirects to [bjptechnologies.co.tz](https://bjptechnologies.co.tz) |

---

## Stack

- Django 5.x LTS, Python 3.11
- MySQL 8 / MariaDB
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

### Local URLs

No `/etc/hosts` setup needed — verticals are URL paths on the single host.

- `http://127.0.0.1:8000/` — hub home
- `http://127.0.0.1:8000/financial/` — Financial Coming Soon
- `http://127.0.0.1:8000/construction/`, `/energies/`, `/farming/`, `/investments/`
- `http://127.0.0.1:8000/technologies/` — 301 to bjptechnologies.co.tz

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
