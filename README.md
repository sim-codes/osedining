# Ose Private Dining

Marketing and booking website for Ose Private Dining (Chef Ehis). Built with
Django, it presents the chef's menus and gallery and lets visitors submit
booking/inquiry forms for private dining services.

**Live site:** [osedining.com](https://osedining.com)

## Table of contents

- [Tech stack](#tech-stack)
- [Folder structure](#folder-structure)
- [Local setup](#local-setup)
- [Common commands](#common-commands)
- [Environment variables](#environment-variables)
- [Routes](#routes)
- [Static files & deployment](#static-files--deployment)
- [Notes](#notes)
- [References](#references)
- [Owner](#owner)

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

## Folder structure

```
osedining/
├── core/                     # Django project package
│   ├── settings.py           # Config, env vars, installed apps, database, email, static files
│   ├── urls.py                # Root URL routing (admin, pages, captcha, letsencrypt, favicon)
│   ├── wsgi.py                 # WSGI entrypoint (used by gunicorn in production)
│   └── asgi.py                  # ASGI entrypoint (async deployment, unused by default)
│
├── pages/                    # Main application — all site content and forms
│   ├── models.py              # Contact, Hire, CustomisedDining, FineDining, CasualDining
│   ├── views.py                 # Page views + booking form handlers
│   ├── forms.py                  # ModelForms for each booking type (with captcha)
│   ├── urls.py                    # App routes, namespaced as `pages`
│   ├── admin.py                    # Django admin registrations (Contact, FineDining, CustomisedDining)
│   ├── apps.py                      # AppConfig
│   ├── tests.py                      # Test stubs
│   ├── static/                # App static assets
│   │   ├── css/                 # Stylesheets (base, about, gallery, menu, dark-mode, lightbox)
│   │   ├── js/                   # Menu interaction + lightbox scripts
│   │   ├── images/                # Logos, hero images, food photography
│   │   │   └── works/               # Gallery photo set (dining event photos, .avif/.webp)
│   │   └── favicon*, apple-touch-icon.png, android-chrome-*.png
│   └── templates/             # Django templates
│       ├── base.html, nav.html, footer.html, 404.html, 500.html
│       ├── pages/                # home, about, menu, gallery, contact, success, hire-a-chef
│       ├── menus/                 # fine dining / casual dining / special menu pages + success pages
│       └── forms/                  # standalone form partials
│
├── bootstrapform/             # Vendored local app — form rendering template filter
│   ├── templatetags/bootstrap.py  # `{{ form|bootstrap }}` filter (see [Notes](#notes))
│   ├── templates/bootstrapform/    # field.html, form.html, formset.html
│   └── config.py                    # BOOTSTRAP_COLUMN_COUNT setting
│
├── public/static/              # Local placeholder for collectstatic output (not the deploy target)
├── manage.py                    # Django management CLI entrypoint
├── requirements.txt               # Pinned Python dependencies
└── .gitignore                      # Excludes .venv, .env, __pycache__, migrations/, *.sqlite3
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

4. **Run migrations and start the server** — see [Common
   commands](#common-commands) below.

## Common commands

Run these from the project root with the virtual environment activated.

| Command | Purpose |
|---|---|
| `python manage.py runserver` | Start the local development server |
| `python manage.py migrate` | Apply database migrations (SQLite when `DEVELOPMENT_MODE=True`) |
| `python manage.py makemigrations pages` | Generate new migrations after changing `pages/models.py` |
| `python manage.py createsuperuser` | Create an admin account for `/admin/` |
| `python manage.py test` | Run the test suite |
| `python manage.py collectstatic` | Collect static files into `STATIC_ROOT` (see [Static files & deployment](#static-files--deployment)) |
| `python manage.py check` | Run Django's system checks |
| `python manage.py shell` | Open an interactive shell with the project loaded |
| `pip install -r requirements.txt` | Install/sync dependencies |
| `gunicorn core.wsgi:application` | Run the production WSGI server |

## Environment variables

| Variable | Purpose | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django `SECRET_KEY` | randomly generated if unset (not safe for production) |
| `DEBUG` | Enables Django debug mode (`"True"`/`"False"`) | `False` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated `ALLOWED_HOSTS` (production: `osedining.com,www.osedining.com`) | `127.0.0.1,localhost` |
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
  `core/settings.py`. The site is live at
  [osedining.com](https://osedining.com) with `django-letsencrypt`
  handling certificates, so it's worth confirming HTTPS is enforced end to
  end and turning these on if not already.

## References

- [Django documentation](https://docs.djangoproject.com/en/5.2/)
- [Django deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [WhiteNoise documentation](https://whitenoise.readthedocs.io/)
- [django-simple-captcha documentation](https://django-simple-captcha.readthedocs.io/)
- [django-letsencrypt on PyPI](https://pypi.org/project/django-letsencrypt/)
- [Gunicorn documentation](https://docs.gunicorn.org/)
- [psycopg2 documentation](https://www.psycopg.org/docs/)

## Owner

Maintained by Michael Ibrahim (Ibrahim Michael)

- Email: [segunmichael24@gmail.com](mailto:segunmichael24@gmail.com)
- Portfolio: [My portfolio](https://simportfolio.netlify.app/)
