Development setup (Linux/Mac)

1) Create and activate venv

```bash
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Configure environment

Copy `.env.example` to `.env` and fill values (see variables inline in settings or below).
If `.env.example` cannot be created in this environment, copy `ENV_EXAMPLE.txt` instead.

Required variables: DJANGO_SECRET_KEY, DJANGO_DEBUG, DJANGO_ALLOWED_HOSTS, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, REDIS_URL, WA_VERIFY_TOKEN, WA_PHONE_ID, WA_BEARER_TOKEN, MEDIA_BASE_URL, OPENAI_API_KEY, OPENAI_MODEL_ID_CLASSIFY, OPENAI_MODEL_ID_CHAT, OPENAI_MODEL_ID_EMBEDDINGS, TOKENS_MAX, RECOS_TOPK, FAQ_TOPK, DIST_REF_EN, DIST_REF_AR, PRODUCT_DOMAIN, DEFAULT_CURRENCY, ORDER_NUMBER_PREFIX, ABANDONED_CART_DAYS, ABANDONED_CHAT_DAYS, SHOPIFY_STORE_URL, SHOPIFY_ACCESS_TOKEN, SHOPIFY_API_VERSION.

LLM provider (optional overrides): LLM_PROVIDER (openai|openrouter|vllm), OPENROUTER_API_KEY, OPENROUTER_BASE_URL, VLLM_BASE_URL, LLM_MODEL_ID_CLASSIFY, LLM_MODEL_ID_CHAT, LLM_REQUEST_TIMEOUT.

4) Initialize database

```bash
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@example.com
```

5) Seed demo data

```bash
python manage.py seed_brandkit
python manage.py seed_inventory
python manage.py seed_helpdesk
python manage.py seed_orders
python manage.py seed_all
```

6) Run services

Terminal 1 (Django):

```bash
python manage.py runserver 0.0.0.0:8000
```

Terminal 2 (Celery worker):

```bash
celery -A project_core.celery worker -l info
```

Terminal 3 (Celery beat):

```bash
celery -A project_core.celery beat -l info
```

7) Tests

```bash
pytest --cov=.
```

8) Makefile shortcuts

```bash
make setup   # venv + install + migrate
make seed    # load sample data
make run     # runserver
make worker  # celery worker
make beat    # celery beat
make test    # pytest with coverage
make lint    # ruff check

9) LLM Providers

- OpenAI (default): set OPENAI_API_KEY and model ids.
- OpenRouter: set LLM_PROVIDER=openrouter and OPENROUTER_API_KEY (optionally OPENROUTER_BASE_URL).
- vLLM (self-hosted): set LLM_PROVIDER=vllm and VLLM_BASE_URL (OpenAI-compatible endpoint like http://localhost:8000/v1).
```


