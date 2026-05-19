from pathlib import Path

import environ
from django.templatetags.static import static
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    DB_PORT=(int, 3306),
    EMAIL_PORT=(int, 587),
    EMAIL_USE_TLS=(bool, True),
)
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "widget_tweaks",
    "apps.core",
    "apps.hub",
    "apps.leads",
    "apps.construction",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.company_info",
                "apps.core.context_processors.app_theme",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASS"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Dar_es_Salaam"
USE_I18N = True
USE_TZ = True

STATIC_URL = env("STATIC_URL", default="/static/")
STATIC_ROOT = BASE_DIR / "public" / "static"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = env("MEDIA_URL", default="/media/")
MEDIA_ROOT = BASE_DIR / "public" / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
CONTACT_EMAIL = env("CONTACT_EMAIL")
LEADS_EMAIL = env("LEADS_EMAIL")

# --- Django Unfold Admin ---


def _bejundas_logo(request):
    return static("images/brand/favicon.svg")


UNFOLD = {
    "SITE_TITLE": "Bejundas Admin",
    "SITE_HEADER": "Bejundas Group of Companies",
    "SITE_URL": "/",
    "SITE_ICON": _bejundas_logo,
    "SITE_LOGO": _bejundas_logo,
    "SITE_SYMBOL": "business",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "DASHBOARD_CALLBACK": "apps.core.admin.dashboard_callback",
    "COLORS": {
        "primary": {
            "50": "239 246 255",
            "100": "219 234 254",
            "200": "191 219 254",
            "300": "147 197 253",
            "400": "96 165 250",
            "500": "59 130 246",
            "600": "37 99 235",
            "700": "29 78 216",
            "800": "30 64 175",
            "900": "30 58 138",
            "950": "23 37 84",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Dashboard",
                "separator": False,
                "items": [
                    {
                        "title": "Overview",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": "Website Content",
                "separator": True,
                "items": [
                    {
                        "title": "Services",
                        "icon": "list_alt",
                        "link": reverse_lazy("admin:hub_service_changelist"),
                    },
                    {
                        "title": "News",
                        "icon": "newspaper",
                        "link": reverse_lazy("admin:hub_news_changelist"),
                    },
                    {
                        "title": "Team Members",
                        "icon": "groups",
                        "link": reverse_lazy("admin:hub_teammember_changelist"),
                    },
                ],
            },
            {
                "title": "Leads",
                "separator": True,
                "items": [
                    {
                        "title": "All Leads",
                        "icon": "inbox",
                        "link": reverse_lazy("admin:leads_lead_changelist"),
                        "badge": "apps.core.admin.unread_leads_badge",
                    },
                    {
                        "title": "Vertical Placeholders",
                        "icon": "category",
                        "link": reverse_lazy("admin:leads_verticalplaceholder_changelist"),
                    },
                ],
            },
            {
                "title": "Site Settings",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Identity & Branding",
                        "icon": "badge",
                        "link": reverse_lazy("admin:core_identitysettings_changelist"),
                    },
                    {
                        "title": "Hero Section",
                        "icon": "web_asset",
                        "link": reverse_lazy("admin:core_herosettings_changelist"),
                    },
                    {
                        "title": "About Section",
                        "icon": "info",
                        "link": reverse_lazy("admin:core_aboutsettings_changelist"),
                    },
                    {
                        "title": "Mission & Vision",
                        "icon": "flag",
                        "link": reverse_lazy("admin:core_missionvisionsettings_changelist"),
                    },
                    {
                        "title": "CTA Section",
                        "icon": "campaign",
                        "link": reverse_lazy("admin:core_ctasettings_changelist"),
                    },
                    {
                        "title": "Contact Info",
                        "icon": "contact_mail",
                        "link": reverse_lazy("admin:core_contactsettings_changelist"),
                    },
                    {
                        "title": "Social Media",
                        "icon": "share",
                        "link": reverse_lazy("admin:core_socialmediasettings_changelist"),
                    },
                ],
            },
            {
                "title": "Administration",
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": "Groups",
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
}
