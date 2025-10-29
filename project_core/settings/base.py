from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

# Core
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-insecure-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() in {"1", "true", "yes", "on"}
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "rest_framework",
    "django_extensions",
    "django_crontab",
    # Local apps (phase ordering roughly by dependencies)
    "site_config",
    "users",
    "brandkit",
    "inventory",
    "orders",
    "payments",
    "conversation_log",
    "recos",
    "helpdesk",
    "wa_gateway",
    "wa_client",
    "message_bus",
    "intent_classifier",
    "ai_assistant",
    "dialog_engine",
    "bootstrap",
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

ROOT_URLCONF = "project_core.urls"

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
    }
]

WSGI_APPLICATION = "project_core.wsgi.application"
ASGI_APPLICATION = "project_core.asgi.application"


# Database (MySQL InnoDB)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME", "commerce_db"),
        "USER": os.environ.get("DB_USER", "root"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "3306"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("en", "English"),
    ("ar", "Arabic"),
]


# Static and media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS: list[Path] = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}


# Celery
CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE


# Caches (Redis)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
    }
}


# WhatsApp Graph API
WA_VERIFY_TOKEN = os.environ.get("WA_VERIFY_TOKEN", "")
WA_PHONE_ID = os.environ.get("WA_PHONE_ID", "")
WA_BEARER_TOKEN = os.environ.get("WA_BEARER_TOKEN", "")
MEDIA_BASE_URL = os.environ.get("MEDIA_BASE_URL", "")


# OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL_ID_CLASSIFY = os.environ.get("OPENAI_MODEL_ID_CLASSIFY", "gpt-4")
OPENAI_MODEL_ID_CHAT = os.environ.get("OPENAI_MODEL_ID_CHAT", "gpt-4")
OPENAI_MODEL_ID_EMBEDDINGS = os.environ.get("OPENAI_MODEL_ID_EMBEDDINGS", "text-embedding-ada-002")


# Business
PRODUCT_DOMAIN = os.environ.get("PRODUCT_DOMAIN", "electronics")
DEFAULT_CURRENCY = os.environ.get("DEFAULT_CURRENCY", "USD")
ORDER_NUMBER_PREFIX = os.environ.get("ORDER_NUMBER_PREFIX", "ORD")


# Thresholds
TOKENS_MAX = int(os.environ.get("TOKENS_MAX", 3000))
RECOS_TOPK = int(os.environ.get("RECOS_TOPK", 5))
FAQ_TOPK = int(os.environ.get("FAQ_TOPK", 3))
DIST_REF_EN = float(os.environ.get("DIST_REF_EN", 0.7))
DIST_REF_AR = float(os.environ.get("DIST_REF_AR", 0.75))


# Housekeeping
ABANDONED_CART_DAYS = int(os.environ.get("ABANDONED_CART_DAYS", 7))
ABANDONED_CHAT_DAYS = int(os.environ.get("ABANDONED_CHAT_DAYS", 30))


# Shopify
SHOPIFY_STORE_URL = os.environ.get("SHOPIFY_STORE_URL", "")
SHOPIFY_ACCESS_TOKEN = os.environ.get("SHOPIFY_ACCESS_TOKEN", "")
SHOPIFY_API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2024-01")


# LLM Provider Configuration
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "openai")  # openai | openrouter | vllm
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
VLLM_BASE_URL = os.environ.get("VLLM_BASE_URL", "")  # e.g., http://localhost:8000/v1
LLM_REQUEST_TIMEOUT = int(os.environ.get("LLM_REQUEST_TIMEOUT", 30))
LLM_MODEL_ID_CLASSIFY = os.environ.get("LLM_MODEL_ID_CLASSIFY", OPENAI_MODEL_ID_CLASSIFY)
LLM_MODEL_ID_CHAT = os.environ.get("LLM_MODEL_ID_CHAT", OPENAI_MODEL_ID_CHAT)


# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}


