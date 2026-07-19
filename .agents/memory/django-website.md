x    ---
name: Django Website Setup
description: Key facts about the Django-based energy company website in website/ directory
---

# Django Website — UZEnergo Ta'minlash

## Runtime
- Port: 8000
- Workflow name: `Django Website`
- Start command: `bash /home/runner/workspace/website/manage_start.sh`
- Django version: 6.0.7, Python 3.13

## Admin credentials
- Username: `admin` (or `DJANGO_ADMIN_USER` env var)
- Password: set via `DJANGO_ADMIN_PASS` env var — if not set, a random password is generated on each start and printed to logs
- **Why:** Hardcoded credentials were a security risk; credentials are now env-driven.

## Package installation
- Python packages installed via `installLanguagePackages({ language: "python", packages: [...] })`
- Packages are in `.pythonlibs/` (uv-managed virtual env)

## Architecture
- Single Django app `main/` handles all models, views, admin
- Multilingual: `_uz`, `_ru`, `_en` field suffixes on every model (NOT django-modeltranslation)
- Language stored in Django session (`request.session['lang']`), default `uz`
- Static files served via WhiteNoise

## How to apply: future changes
- New multilingual fields → add `_uz`, `_ru`, `_en` variants; run `makemigrations && migrate`
- Admin changes → edit `website/main/admin.py`
- After code changes → restart workflow "Django Website"
- Initial data seeding is idempotent (checks `.exists()` before creating)
