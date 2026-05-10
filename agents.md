# AGENTS.md

You are building **dwi.ma**, a Moroccan Darija AI SaaS that helps users understand documents and generate useful messages.

This file contains the project-specific rules Codex must follow while working in this repository.

---

## 1. Product Summary

dwi.ma is a mobile-first PWA and WhatsApp companion service for Morocco.

The MVP focuses on:

1. Explaining documents in simple Moroccan Darija.
2. Explaining pasted French/Arabic/formal text in simple Moroccan Darija.
3. Turning Darija text or voice notes into professional messages.
4. Sending results to a WhatsApp number.
5. Using a credit/payment system through Digital Virgo.

The product must **not** be built as a generic chatbot in the MVP.

---

## 2. Core Stack

Use the following stack unless the user explicitly changes it:

- Python 3.12+
- Django 5.x
- Django Ninja for API endpoints
- PostgreSQL
- Celery + Redis for background jobs
- Django templates
- Bootstrap 5
- HTMX for lightweight interactivity
- Alpine.js only when needed
- WhatsApp Business API
- Digital Virgo payment API
- OpenAI/Anthropic for MVP AI providers
- S3-compatible storage for production file storage

---

## 3. Required Django Apps

Create and maintain this modular structure:

```text
apps/
  accounts/
  wallet/
  payments/
  whatsapp/
  documents/
  audio/
  assistant/
  notifications/
  core/
```

Responsibilities:

- `accounts`: users, profiles, phone identity, consent logs.
- `wallet`: credit balance, usage events, refunds, adjustments.
- `payments`: payment products, Digital Virgo transactions, payment callbacks.
- `whatsapp`: inbound/outbound WhatsApp messages, webhook events, send services.
- `documents`: uploaded documents, extracted text, document analyses.
- `audio`: voice notes and transcription jobs.
- `assistant`: AI jobs, prompt templates, AI provider services, safety flags.
- `notifications`: outbound user notifications.
- `core`: audit logs, system settings, shared utilities.

---

## 4. MVP Boundaries

Build step by step.

Do implement:

- Phone-number-first user model.
- Mobile-first web UI.
- Document upload.
- Text extraction from PDFs when possible.
- AI document explanation in Darija.
- Pasted text explanation.
- Darija-to-professional-message generation.
- WhatsApp result delivery.
- Credit wallet.
- Digital Virgo payment skeleton.
- Admin visibility.
- Privacy consent and document deletion.

Do **not** implement yet:

- Native Android/iOS app.
- React or Next.js frontend.
- Self-hosted Atlas model.
- Generic open-ended chatbot.
- Inwi white-label dashboard.
- Full Moroccan government procedure RAG.
- Medical diagnosis.
- Legal advice.
- Accounting automation.
- Human expert marketplace.

---

## 5. Coding Rules

1. Keep views thin. Put business logic in services.
2. Keep provider-specific code isolated.
3. All heavy work must run in Celery tasks.
4. Webhooks must return quickly.
5. Use environment variables for all secrets.
6. Never hard-code API keys.
7. Use UUIDs for externally referenced objects.
8. Add indexes on `user`, `status`, `created_at`, provider transaction IDs, and WhatsApp message IDs.
9. Use database transactions for wallet charging and payment callbacks.
10. Make payment callbacks idempotent.
11. Failed AI jobs must not consume credits.
12. Do not delete DB records for user files; mark them deleted and remove the physical file.
13. Add tests for every milestone.
14. Prefer clear, boring, maintainable code over clever abstractions.

---

## 6. AI Behavior Rules

The assistant must:

- Explain documents in simple Moroccan Darija.
- Avoid formal Arabic unless the user requests it.
- Never invent information not found in the source document/text.
- Say exactly: `هاد النقطة ما واضحةش فهاد الوثيقة.` when something is unclear.
- Extract names, dates, amounts, obligations, and deadlines when available.
- Tell the user what they may need to do next.
- Add a disclaimer for legal, medical, financial, insurance, banking, tax, employment, or administrative documents.
- Never provide final legal, medical, or financial advice.
- Return structured JSON where specified by the prompt.

---

## 7. Prompt and Provider Rules

- Store reusable prompts in `apps/assistant/prompts/` or a dedicated prompt service.
- Use prompt versioning.
- Save AI job metadata:
  - provider
  - model
  - prompt version
  - status
  - latency
  - error message
  - cost estimate if available
- Use a mock AI provider in tests.
- Do not call real AI providers in automated tests.

---

## 8. WhatsApp Rules

- WhatsApp is a companion interface, not the full product.
- Use task-specific menus:
  - Explain document
  - Explain text
  - Write message
  - Check credits
  - Pricing
- Do not position the WhatsApp bot as “ask anything.”
- Store raw webhook payloads for debugging.
- Validate webhook requests when credentials are configured.
- Acknowledge webhooks quickly, then process asynchronously.
- Use service functions for sending messages.

---

## 9. Payment Rules

- Keep Digital Virgo logic isolated in `apps/payments/services/`.
- Create a pending transaction before sending the user to payment.
- Verify provider callback signatures when real credentials are available.
- Store raw callback payloads.
- Payment callback must be idempotent.
- Never credit the same provider transaction twice.
- Add credits only after verified successful payment.

---

## 10. Privacy and Safety Rules

- Ask for consent before processing uploaded documents.
- Store consent logs.
- Allow users to delete uploaded documents.
- Do not use user documents for model training by default.
- Store original files temporarily.
- Use private file storage.
- Add audit logs for sensitive operations.
- Add disclaimers in high-risk document categories.

---

## 11. Testing Requirements

At minimum, add tests for:

- Project loads correctly.
- Custom user model works.
- Wallet free credit grant.
- Wallet charge/refund behavior.
- Failed AI job does not deduct credits.
- Document upload validation.
- Text PDF extraction flow.
- AI JSON parsing failure handling.
- WhatsApp webhook stores event and returns quickly.
- Digital Virgo callback idempotency.
- Document deletion removes file and marks DB record deleted.

---

## 12. Reference Documents

Before implementing a milestone, read:

- `product/PRD.md`
- `product/ARCHITECTURE.md`
- `product/API_SPEC.md`
- `product/PROMPTS.md`
- `product/WHATSAPP_FLOWS.md`
- `product/PAYMENT_SPEC.md`
- `product/SECURITY_PRIVACY.md`

---

## 13. Milestone Discipline

When asked to implement a milestone:

1. Read the relevant docs.
2. Summarize the scope.
3. Implement only that milestone.
4. Do not add future features.
5. Run or describe tests.
6. Explain changed files.
7. Mention any assumptions or TODOs clearly.
