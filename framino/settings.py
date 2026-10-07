"""
Django settings for framino project.

Technical settings (timezone, port, multi-postes) are read from
config/environnement.toml. Business values live in config/parametres.toml
and are loaded by the `parametres` app, never here.
"""

import sys
import tomllib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- config/environnement.toml ------------------------------------------------

with open(BASE_DIR / "config" / "environnement.toml", "rb") as f:
    ENVIRONNEMENT = tomllib.load(f)

SECRET_KEY = "django-insecure-local-only-framino"
DEBUG = True

# multi_postes = true -> reachable from other machines on the local network
if ENVIRONNEMENT.get("multi_postes", False):
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Project apps
    "parametres",
    "accounts",
    "personnel",
    "clients",
    "abonnements",
    "visites",
    "services",
    "stock",
    "materiel",
    "caisse",
    "charges",
    "dashboard",
    "backup",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "framino.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.role",
            ],
        },
    },
]

WSGI_APPLICATION = "framino.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fr-FR"
TIME_ZONE = ENVIRONNEMENT.get("fuseau_horaire", "Africa/Douala")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "accounts:login"

# Server port (used by start scripts and runserver default)
PORT = ENVIRONNEMENT.get("port", 8000)

if "test" in sys.argv or "pytest" in sys.modules:
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]