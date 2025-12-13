from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-REEMPLAZAR_ESTO_EN_PRODUCCION'

# En producción este debe estar False; lo mantenemos en False para mostrar errores personalizados.
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# ============================
# Seguridad / Proxy / CSRF
# ============================
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    "https://127.0.0.1",
    "https://localhost",
]

# ============================
# APPS
# ============================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "app_core",
    "api",

    "drf_spectacular",
    "sslserver",
]

# ============================
# MIDDLEWARE
# ============================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # Nuestro middleware de reporte de errores debe ir **antes** de la gestión final de excepciones
    "app_core.middleware.ErrorReportingMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mi_proyecto.urls"

# ============================
# TEMPLATES
# ============================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "app_core" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mi_proyecto.wsgi.application"

# ============================
# BASE DE DATOS
# ============================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ============================
# PASSWORD VALIDATION
# ============================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ============================
# INTERNACIONALIZACIÓN
# ============================
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# ============================
# STATIC / MEDIA
# ============================
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "app_core" / "static"
]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ============================
# DRF + SWAGGER
# ============================
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Evaluación 3 - API",
    "DESCRIPTION": "Documentación automática generada con OpenAPI 3.",
    "VERSION": "1.0.0",
}

# ============================
# LOGGING PROFESIONAL
# ============================
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "detailed": {
            "format": "[{asctime}] [{levelname}] {name}: {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
        },
        "file_app": {
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "app.log"),
            "formatter": "detailed",
            "level": "INFO",
        },
        "file_errors": {
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "errors.log"),
            "formatter": "detailed",
            "level": "ERROR",
        },
        "file_kafka": {
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "kafka.log"),
            "formatter": "detailed",
            "level": "INFO",
        },
    },

    "loggers": {
        "django": {
            "handlers": ["console", "file_app"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["file_errors"],
            "level": "ERROR",
            "propagate": False,
        },
        "app_core": {
            "handlers": ["console", "file_app"],
            "level": "INFO",
            "propagate": False,
        },
        "api": {
            "handlers": ["console", "file_app"],
            "level": "INFO",
            "propagate": False,
        },
        "kafka": {
            "handlers": ["file_kafka", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# SSL (valores existentes, por si usas runsslserver)
SSL_CERTIFICATE = str(BASE_DIR / "ssl.crt")
SSL_KEY = str(BASE_DIR / "ssl.key")
