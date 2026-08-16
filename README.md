# Ose Private Dining

Marketing and booking website for Ose Private Dining (Chef Ehis). Built with
Django, it presents the chef's menus and gallery and lets visitors submit
booking/inquiry forms for private dining services.

## Tech stack

- **Python** 3.14
- **Django** 5.2 (LTS)
- **Database**: PostgreSQL in production (`psycopg2-binary`), SQLite in
  development
- **Static files**: WhiteNoise (`CompressedManifestStaticFilesStorage`)
- **Forms**: `django-simple-captcha` for spam protection; form styling via a
  locally vendored `bootstrapform` app (see [Notes](#notes))
- **TLS**: `django-letsencrypt` for ACME challenge handling
- **App server**: Gunicorn (WSGI)

## Project layout

```
core/            Django project settings, URL routing, WSGI/ASGI entrypoints
pages/           Main application: models, views, forms, templates, static assets
bootstrapform/   Vendored local app providing the `{{ form|bootstrap }}` template filter
public/          Deployment-time static file output (populated by collectstatic)
manage.py        Django management CLI entrypoint
requirements.txt Pinned dependencies
```

## Local setup

1. **Create a virtual environment** (Python 3.14):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # macOS/Linux
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the project root (see [Environment
   variables](#environment-variables) below for the full list). For local
   development at minimum:

   ```
   DEVELOPMENT_MODE=True
   DEBUG=True
   DJANGO_SECRET_KEY=your-local-secret-key
   DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
   HOST_USER=you@example.com
   HOST_PASSWORD=your-smtp-password
   ```

   `HOST_USER`/`HOST_PASSWORD` are required even in development because the
   email backend is always SMTP (`smtp.privateemail.com`) — there's no
   console-email fallback for local runs.

4. **Run migrations** (uses SQLite when `DEVELOPMENT_MODE=True`):

   ```bash
   python manage.py migrate
   ```

5. **Create an admin user**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the dev server**:

   ```bash
   python manage.py runserver
   ```

## Environment variables

| Variable | Purpose | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django `SECRET_KEY` | randomly generated if unset (not safe for production) |
| `DEBUG` | Enables Django debug mode (`"True"`/`"False"`) | `False` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated `ALLOWED_HOSTS` | `127.0.0.1,localhost` |
| `DEVELOPMENT_MODE` | When `"True"`, uses local SQLite instead of Postgres | `False` |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD` | PostgreSQL credentials (required unless `DEVELOPMENT_MODE=True`); host is hardcoded to `localhost` | — |
| `HOST_USER` | SMTP username; also used as the from-address and notification recipient | — |
| `HOST_PASSWORD` | SMTP password | — |

## Routes

| Path | Purpose |
|---|---|
| `/` | Home |
| `/about/` | About / chef bio |
| `/menu/` | Menu |
| `/gallery/` | Gallery |
| `/contact/` | Contact form → `/success/` |
| `/hire-a-chef/` | Hire-a-chef booking form → `/hire-a-chef/successful` |
| `/finedining/` | Fine dining booking form → `/finedining/successful/` |
| `/casual-dining/` | Casual dining booking form → `/casual-dining/successful/` |
| `/custom-dining/` | Custom dining booking form → `/custom-dining/successful/` |
| `/admin/` | Django admin |
| `/captcha/` | django-simple-captcha endpoints |
| `/.well-known/` | Let's Encrypt ACME challenge routes |

## Static files & deployment

`STATIC_ROOT` is hardcoded to `/var/www/html/osedining/public/static`,
matching the production server's directory layout. Running
`python manage.py collectstatic` locally will attempt to write there and
fail unless that path exists or `STATIC_ROOT` is overridden — override it
locally if you need to run `collectstatic` outside the production host.

In production, the process is expected to run behind Gunicorn:

```bash
gunicorn core.wsgi:application
```

with PostgreSQL configured via the `DB_*` environment variables and a
reverse proxy (e.g. nginx) in front, using `django-letsencrypt` for
certificate renewal.

## Notes

- `bootstrapform` is a local app, not a PyPI dependency. The upstream
  `django-bootstrap-form` package is unmaintained and breaks on Python
  3.12+ (it imports `distutils`, which was removed from the standard
  library). Only the one broken import was stripped out — the templates
  and filter behavior are unchanged, so `{% load bootstrap %}` /
  `{{ form|bootstrap }}` in templates work exactly as before.
- Several packages in `requirements.txt` (PDF generation, cryptographic
  signing, QR codes, HTML parsing) aren't currently imported anywhere in
  `pages/` or `core/` — they appear to be either leftover from removed
  features or transitive dependencies frozen alongside direct ones. They're
  kept as-is but may be worth auditing if you're trimming the dependency
  footprint.
- HTTPS-hardening settings (`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`,
  `SECURE_HSTS_*`, `CSRF_COOKIE_SECURE`) are present but commented out in
  `core/settings.py` — enable them once the production domain is served
  over HTTPS.
