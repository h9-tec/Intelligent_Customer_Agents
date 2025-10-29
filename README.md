## Conversational Commerce Backend (Electronics Domain)

This repository implements a production‑grade conversational commerce backend specialized for the electronics domain. It powers an end‑to‑end WhatsApp commerce experience: inbound webhook → intent classification → recommendations via local transformer embeddings → cart and orders → outbound messaging via the WhatsApp Graph API. It also integrates with Shopify Admin for catalog sync.

### Key Features

- **Modular Django 4.2**: 15+ decoupled apps for config, users, brandkit, inventory, orders, payments, conversation logs, embeddings, helpdesk, WA gateway/client, message bus, intent classifier, AI assistant, dialog engine, and bootstrap seeders.
- **MySQL (InnoDB)**: Strict transactions, FK constraints, and indices on hot fields (phone, SKU, order_number).
- **Celery + Redis**: Asynchronous processing, scheduled housekeeping, and management commands.
- **Local embeddings**: Sentence-Transformers with multilingual models (EN/AR), cosine similarity and configurable thresholds.
- **WhatsApp Graph API**: Token verification, webhook ingestion, message dispatch (text, buttons, lists, images).
- **OpenAI GPT**: Intent classification, assistant responses, and structured comparison flows.
- **Shopify Admin**: Basic product sync with electronics-specific fields.

## Architecture Overview

- **Messaging pipeline**: WhatsApp Webhook → Celery task → Django signal → Dialog Engine → State handlers → Message Bus → WhatsApp Client.
- **AI layer**: Intent classifier (OpenAI) + local product/FAQ embeddings (Sentence-Transformers) + assistant context windowing.
- **Commerce core**: Inventory (electronics), carts, orders, payments; utilities for validation and totals.
- **Extensibility**: Pluggable states (35+ planned), i18n templates (EN/AR), Shopify connectors.

## Tech Stack

- Django 4.2, DRF 3.14
- MySQL 8+ (InnoDB)
- Celery 5.3 + Redis 5
- OpenAI Python SDK 1.x
- sentence-transformers 2.x, torch 2.x
- PyTest, Ruff, MyPy (optional)

## Repository Structure

```text
project_core/           # Settings split, Celery app, URLs, WSGI/ASGI
site_config/            # Singleton site configuration
users/                  # Customer model and utilities
brandkit/               # Brand profile, taxonomy, features
inventory/              # Electronics domain models (Category, Product, names/descriptions)
orders/                 # ShippingOption, Cart, CartItem, Order, utils, tasks
payments/               # PaymentOptions, Payment, admin
conversation_log/       # Chat and Message logs, cleanup tasks
recos/                  # Product embeddings, recommender, trainer command
helpdesk/               # FAQ + embeddings, recommender, trainer command
wa_gateway/             # Webhook views, message types, Celery task
wa_client/              # WhatsApp Graph client and endpoints
message_bus/            # DTOs, i18n templates, composer (persist + dispatch)
intent_classifier/      # OpenAI-based intent classification
ai_assistant/           # Context, related info, compare, recommend orchestration
dialog_engine/          # Signal, engine, state router, sample states
connectors/shopify_admin/ # Shopify REST client + product sync
bootstrap/management/commands/ # Seeders and utilities
tests/                  # PyTest suite and fixtures
docs/SETUP.md           # Setup notes
Makefile                # Common commands
```

## Getting Started

### Prerequisites

- Python 3.10+
- MySQL 8+ (with InnoDB)
- Redis 6+

### Environment Variables

If you cannot create hidden files in your environment, use `ENV_EXAMPLE.txt` as a reference and copy it to `.env` manually. Variables include:

```ini
# Django
DJANGO_SECRET_KEY=
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=commerce_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306

# Redis/Celery
REDIS_URL=redis://localhost:6379/0

# WhatsApp
WA_VERIFY_TOKEN=
WA_PHONE_ID=
WA_BEARER_TOKEN=
MEDIA_BASE_URL=

# OpenAI
OPENAI_API_KEY=
OPENAI_MODEL_ID_CLASSIFY=gpt-4
OPENAI_MODEL_ID_CHAT=gpt-4
OPENAI_MODEL_ID_EMBEDDINGS=text-embedding-ada-002

# LLM Provider (OpenAI default, or OpenRouter/vLLM)
LLM_PROVIDER=openai   # openai|openrouter|vllm
OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
VLLM_BASE_URL=http://localhost:8000/v1
LLM_MODEL_ID_CLASSIFY=
LLM_MODEL_ID_CHAT=
LLM_REQUEST_TIMEOUT=30

# Business
PRODUCT_DOMAIN=electronics
DEFAULT_CURRENCY=USD
ORDER_NUMBER_PREFIX=ORD

# Thresholds
TOKENS_MAX=3000
RECOS_TOPK=5
FAQ_TOPK=3
DIST_REF_EN=0.7
DIST_REF_AR=0.75

# Housekeeping
ABANDONED_CART_DAYS=7
ABANDONED_CHAT_DAYS=30

# Shopify
SHOPIFY_STORE_URL=
SHOPIFY_ACCESS_TOKEN=
SHOPIFY_API_VERSION=2024-01
```

### Database Setup (MySQL)

```sql
CREATE DATABASE commerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'root'@'%' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON commerce_db.* TO 'root'@'%';
FLUSH PRIVILEGES;
```

### Installation

```bash
make setup      # venv + install + migrate
make seed       # seed demo data (brandkit, inventory, helpdesk, orders)
```

Run services (three terminals):

```bash
make run        # Django dev server
make worker     # Celery worker
make beat       # Celery beat
```

### Embeddings

Generate local embeddings when ready:

```bash
python manage.py train_product_embeddings
python manage.py train_faq_embeddings
```

### Tests & Linting

```bash
make test       # pytest with coverage
make lint       # ruff check
```

## URLs & API Contracts

- Admin: `/admin/`
- WhatsApp Webhook: `/hook/`
  - GET verification: `/hook/verify/?hub.verify_token=...&hub.challenge=...`
  - POST messages: Facebook Graph API compliant payloads (v16+)
- API root (future expansion): `/api/`

### WhatsApp Verification

Responds with the `hub.challenge` when `hub.verify_token` matches `WA_VERIFY_TOKEN`.

### Inbound Message Handling

Incoming `text` and `interactive` events are parsed and enqueued to Celery. A Django signal triggers the Dialog Engine, which routes to states and returns outbound DTOs dispatched by the WhatsApp client.

## Dialog Engine & States

- Entry: `dialog_engine.engine.ChatEngine.handle_message(event)`
- Routing: `dialog_engine.state_router` maps state names and button prefixes.
- Minimal states included: `AssistantState`, `ShowCartState`, `CheckoutState` (extend to 35+ states as needed).

## Recommendations & Helpdesk

- Models store embeddings in `BinaryField` as NumPy float32.
- Recommender performs cosine similarity with language‑specific thresholds.
- Helpdesk recommends FAQs with distance filtering and multilingual support.

## Shopify Integration

- Configure `SHOPIFY_STORE_URL`, `SHOPIFY_ACCESS_TOKEN`, `SHOPIFY_API_VERSION`.
- Basic sync utility provided:

```python
# Django shell
from connectors.shopify_admin.product_sync import sync_products
sync_products()
```

Adapt mapping for collections, variants, and metafields to your store.

## Operations & Environments

- Default settings: `project_core.settings.dev`. For production, set `DJANGO_SETTINGS_MODULE=project_core.settings.prod`.
- Production hardening in `prod.py`: SSL redirect, HSTS, secure cookies; set `DJANGO_ALLOWED_HOSTS` properly.
- Celery eager mode (dev/testing) via env: `CELERY_TASK_ALWAYS_EAGER=1`.
- LLM Provider selection: set `LLM_PROVIDER` to `openai`, `openrouter`, or `vllm`. Models: `LLM_MODEL_ID_CLASSIFY`, `LLM_MODEL_ID_CHAT`.

## Troubleshooting

- mysqlclient build issues: ensure MySQL dev headers are installed (e.g., `libmysqlclient-dev`).
- torch install size: consider CUDA/CPU variants per environment constraints.
- Redis connection errors: verify `REDIS_URL` and that Redis is running.
- WhatsApp 401/403: double‑check `WA_BEARER_TOKEN`, `WA_PHONE_ID`, and app permissions.
- OpenAI network errors: code gracefully falls back; verify `OPENAI_API_KEY` and outbound access.
- OpenRouter: ensure `OPENROUTER_API_KEY` and base URL; check quota and headers.
- vLLM: verify `VLLM_BASE_URL` points to OpenAI-compatible `/v1` endpoint; check CORS and auth if enabled.

## Contributing

- Extend dialog states in `dialog_engine/states/**` and register in `state_router`.
- Add admin list/search to keep operations fast.
- Write tests for each new state and business utility.

## Roadmap

- Full 35+ state machine coverage (cart, checkout, FAQ, comparison, reset, etc.).
- Rich product lists and media templates on WhatsApp.
- Advanced Shopify sync (collections, variants, inventory levels, metafields).


