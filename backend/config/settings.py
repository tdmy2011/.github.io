"""
YigeWorks SaaS Platform -- Settings
Django 6.0 生产级配置
"""

import os
from pathlib import Path
from decouple import config, Csv

# ============================================================
# Paths
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# Security & Environment
# ============================================================
SECRET_KEY = config("DJANGO_SECRET_KEY", default="change-me-in-production!!!")

DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="yigeworks.com,www.yigeworks.com,localhost,127.0.0.1", cast=Csv())

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="https://yigeworks.com,https://www.yigeworks.com", cast=Csv())

# HTTPS 强制 (生产环境)
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# ============================================================
# Application
# ============================================================
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_countries",
]

LOCAL_APPS = [
    "apps.core",
    "apps.marketplace",
    "apps.thinktank",
    "apps.marketing",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",       # 静态文件加速
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.marketing.middleware.GeoVisitorMiddleware",   # Geo 访客追踪
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
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ============================================================
# Database
# ============================================================
# 本地开发 / CI 环境自动使用 SQLite，
# 生产环境使用 PostgreSQL (容器内 db host)
IS_DEV = DEBUG or config("DJANGO_DEV", default=False, cast=bool)

if IS_DEV:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("POSTGRES_DB", default="yigeworks"),
            "USER": config("POSTGRES_USER", default="yigeworks"),
            "PASSWORD": config("POSTGRES_PASSWORD", default=""),
            "HOST": config("POSTGRES_HOST", default="db"),
            "PORT": config("POSTGRES_PORT", default="5432"),
            "CONN_MAX_AGE": 600,
            "OPTIONS": {
                "connect_timeout": 10,
            },
        }
    }

# ============================================================
# Cache (Redis / Dev: LocMem)
# ============================================================
REDIS_URL = config("REDIS_URL", default="redis://redis:6379/0")

if IS_DEV:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        }
    }

# ============================================================
# Celery
# ============================================================
CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="redis://redis:6379/1")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="redis://redis:6379/2")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30分钟超时
CELERY_BEAT_SCHEDULE = {
    # 每日 Geo 报告 (每天 08:00 Asia/Shanghai)
    "daily-geo-report": {
        "task": "marketing.daily_geo_report",
        "schedule": 86400.0,
    },
    # 弃单挽回检查 (每小时)
    "check-abandoned-intents": {
        "task": "marketing.check_abandoned_intents",
        "schedule": 3600.0,
    },
    # 30天复购激活 (每天)
    "check-reengagement": {
        "task": "marketing.check_reengagement",
        "schedule": 86400.0,
    },
}

# ============================================================
# REST Framework
# ============================================================
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
}

# ============================================================
# GeoIP & GDPR
# ============================================================
GEOIP_PATH = config("GEOIP_PATH", default=BASE_DIR / "geoip")

# GDPR 隐私政策 URL
PRIVACY_POLICY_URL = config(
    "PRIVACY_POLICY_URL",
    default="https://yigeworks.com/privacy.html",
)

# Admin 路径 (非默认 /admin/)
ADMIN_PATH = config("DJANGO_ADMIN_PATH", default="admin/")

# ============================================================
# Internationalization
# ============================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("en", "English"),
    ("zh-hans", "简体中文"),
    ("vi", "Tiếng Việt"),
    ("th", "ภาษาไทย"),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

# ============================================================
# Static Files (WhiteNoise)
# ============================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ============================================================
# Media
# ============================================================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ============================================================
# Email (SendGrid / SMTP)
# ============================================================
EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = config("EMAIL_HOST", default="smtp.sendgrid.net")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="apikey")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@yigeworks.com")

# ============================================================
# Logging
# ============================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "yigeworks.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": config("LOG_LEVEL", default="INFO"),
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "celery": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "apps.marketing": {"handlers": ["console", "file"], "level": "DEBUG", "propagate": False},
    },
}

# ============================================================
# Marketing / Email Settings
# ============================================================
UNSUBSCRIBE_BASE_URL = config(
    "UNSUBSCRIBE_BASE_URL",
    default="https://yigeworks.com/unsubscribe/",
)

# ============================================================
# Default Auto Field
# ============================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
