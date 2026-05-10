# dwi.ma Architecture

## 1. Architecture Principle

dwi.ma should be built as a modular Django system with asynchronous processing.

The PWA is the main product surface. WhatsApp is a companion channel for onboarding, task entry, and result delivery.

Heavy tasks such as document parsing, audio transcription, LLM calls, and payment verification must run outside the request/response cycle using Celery.

---

## 2. High-Level Architecture

```text
Mobile PWA / WhatsApp
        |
        v
Django + Django Ninja API
        |
        +--> PostgreSQL
        |
        +--> Redis
        |
        +--> Celery Workers
        |
        +--> Object Storage
        |
        +--> AI Provider Layer
        |       +--> Speech-to-text
        |       +--> PDF/Vision model
        |       +--> LLM reasoning
        |
        +--> WhatsApp Business API
        |
        +--> Digital Virgo API
```

---

## 3. Main Components

### PWA

The PWA handles:

- Landing page.
- User dashboard.
- Document upload.
- Text explanation.
- Message generation.
- Wallet and pricing.
- Result history.
- Payment screens.
- Privacy/terms.

Recommended stack:

- Django templates
- Bootstrap 5
- HTMX
- Minimal Alpine.js
- PWA manifest
- Service worker for installable shell

### Django API

Django Ninja exposes endpoints for:

- Auth/profile.
- Document upload.
- AI job creation.
- Result retrieval.
- WhatsApp actions.
- Payment actions.

### Celery Workers

Celery handles:

- Document extraction.
- AI document explanation.
- Text explanation.
- Audio transcription.
- Message generation.
- WhatsApp webhook processing.
- Payment verification retries.

### PostgreSQL

Stores:

- Users.
- Wallets.
- Documents metadata.
- Extracted text.
- AI jobs.
- WhatsApp events.
- Payment transactions.
- Consent logs.
- Audit logs.

### Object Storage

Stores:

- Uploaded PDFs.
- Uploaded images.
- Audio files.
- Temporary extracted artifacts.

Production should use private S3-compatible storage.

### AI Provider Layer

The provider layer hides details of OpenAI, Anthropic, or future Atlas/self-hosted models.

Required design:

```text
assistant/services/
  providers/
    base.py
    mock.py
    openai_provider.py
    anthropic_provider.py
  prompts/
    document_explanation.py
    message_generation.py
    intent_detection.py
```

### WhatsApp Layer

The WhatsApp module handles:

- Webhook verification.
- Raw event storage.
- Inbound message normalization.
- Media download.
- Outbound message sending.
- Interactive menus.

### Payment Layer

The payment module handles:

- Product catalog.
- Transaction creation.
- Digital Virgo API interaction.
- Callback verification.
- Idempotent credit activation.

---

## 4. Django Apps

```text
apps/accounts
apps/wallet
apps/payments
apps/whatsapp
apps/documents
apps/audio
apps/assistant
apps/notifications
apps/core
```

### accounts

Models:

- User
- Profile
- PhoneIdentity
- ConsentLog

### wallet

Models:

- CreditWallet
- UsageEvent
- CreditAdjustment

### payments

Models:

- PaymentProvider
- PaymentProduct
- PaymentTransaction
- PaymentWebhookEvent

### whatsapp

Models:

- WhatsAppContact
- WhatsAppWebhookEvent
- WhatsAppInboundMessage
- WhatsAppOutboundMessage

### documents

Models:

- UploadedDocument
- ExtractedText
- DocumentAnalysis

### audio

Models:

- VoiceNote
- TranscriptionJob

### assistant

Models:

- AIJob
- PromptTemplate
- AIResponse
- SafetyFlag
- UserFeedback

### notifications

Models:

- Notification
- DeliveryStatus

### core

Models:

- AuditLog
- SystemSetting

---

## 5. Processing Flows

### Document explanation flow

```text
User uploads document
  |
  v
Create UploadedDocument
  |
  v
Create AIJob / queue Celery task
  |
  v
Extract text if possible
  |
  v
If extraction insufficient, use PDF/vision provider
  |
  v
Generate Darija explanation
  |
  v
Validate JSON output
  |
  v
Save DocumentAnalysis
  |
  v
Charge credits
  |
  v
Show result / send WhatsApp
```

### WhatsApp webhook flow

```text
WhatsApp sends webhook
  |
  v
Django endpoint validates/stores payload
  |
  v
Return 200 quickly
  |
  v
Celery parses event
  |
  v
Find/create user
  |
  v
Detect intent
  |
  v
Run task or send menu
```

### Payment callback flow

```text
Digital Virgo callback
  |
  v
Store raw callback
  |
  v
Verify signature/status
  |
  v
Find transaction
  |
  v
Check idempotency
  |
  v
Mark paid
  |
  v
Add credits
  |
  v
Notify user
```

---

## 6. Environment Variables

```env
DJANGO_SECRET_KEY=
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=
REDIS_URL=

OPENAI_API_KEY=
ANTHROPIC_API_KEY=
DEFAULT_LLM_PROVIDER=anthropic
DEFAULT_LLM_MODEL=
TRANSCRIPTION_PROVIDER=openai
TRANSCRIPTION_MODEL=gpt-4o-mini-transcribe

WHATSAPP_VERIFY_TOKEN=
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_BUSINESS_ACCOUNT_ID=
WHATSAPP_APP_SECRET=

DIGITAL_VIRGO_API_BASE_URL=
DIGITAL_VIRGO_MERCHANT_ID=
DIGITAL_VIRGO_API_KEY=
DIGITAL_VIRGO_WEBHOOK_SECRET=

STORAGE_BACKEND=local
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_ENDPOINT_URL=

DEFAULT_FREE_CREDITS=3
DOCUMENT_MAX_UPLOAD_MB=10
ORIGINAL_FILE_RETENTION_DAYS=30
```

---

## 7. Deployment Notes

MVP deployment can start with:

- One VPS for Django + Celery + Redis.
- Managed or separate PostgreSQL if possible.
- S3-compatible object storage.
- Nginx + Gunicorn/Uvicorn.
- HTTPS certificate.

Later split:

- Web server.
- Worker server.
- DB server.
- Object storage.
- Monitoring/logging service.

---

## 8. Key Architecture Risks

### Risk: Webhook timeout

Mitigation: store event and return 200 immediately.

### Risk: Payment double-credit

Mitigation: unique provider transaction ID + database transaction + idempotency check.

### Risk: AI hallucination

Mitigation: structured prompts, source-only answering, JSON validation, unclear-points field.

### Risk: File privacy

Mitigation: private storage, consent logs, delete feature, retention policy.

### Risk: AI provider lock-in

Mitigation: provider abstraction with mock, OpenAI, Anthropic, and future Atlas provider.
