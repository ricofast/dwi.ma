# dwi.ma

**dwi.ma** is a Moroccan Darija AI SaaS that helps users understand documents and generate practical messages.

The MVP is a lightweight mobile-first PWA with a WhatsApp Business API companion and Digital Virgo payment integration.

---

## Product Goal

Help ordinary Moroccan users:

- Upload a document and understand it in simple Moroccan Darija.
- Paste French/Arabic/formal text and receive a clear Darija explanation.
- Send Darija instructions or voice notes and receive professional messages in French, Arabic, or polished WhatsApp style.
- Receive results through WhatsApp.
- Pay using mobile-friendly credits.

---

## MVP Features

1. Explain document in Darija.
2. Explain pasted text in Darija.
3. Generate professional message from Darija input.
4. Send result to WhatsApp.
5. Manage free and paid credits.
6. Process payments through Digital Virgo.
7. Allow document deletion and privacy consent.
8. Provide admin visibility into jobs, payments, users, and errors.

---

## Tech Stack

- Python 3.12+
- Django 5.x
- Django Ninja
- PostgreSQL
- Celery
- Redis
- Bootstrap 5
- HTMX
- WhatsApp Business API
- Digital Virgo API
- OpenAI / Anthropic for MVP AI services
- S3-compatible storage for production

---

## Recommended Repository Structure

```text
dwi_ma/
  AGENTS.md
  README.md
  product/
    PRD.md
    ARCHITECTURE.md
    API_SPEC.md
    PROMPTS.md
    WHATSAPP_FLOWS.md
    PAYMENT_SPEC.md
    SECURITY_PRIVACY.md
  config/
    settings/
      base.py
      local.py
      production.py
    urls.py
    celery.py
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
  templates/
  static/
  tests/
```

---

## Recommended Development Workflow

Do not ask Codex to build the full product at once.

Use this workflow:

1. Add `AGENTS.md` and the `product/` documentation files.
2. Ask Codex to read and summarize the MVP.
3. Ask Codex to propose milestones.
4. Implement one milestone at a time.
5. Review the diff and tests before moving forward.

---

## First Prompt for Codex

```text
Read AGENTS.md and the files in product/.

Do not write code yet.

Your task:
1. Summarize the MVP scope.
2. Propose the first 5 development milestones.
3. Identify missing technical decisions.
4. Propose the initial Django project structure.
5. Confirm what you will implement first.
```

---

## First Implementation Prompt

```text
Implement Milestone 1 only: Django project foundation.

Do not implement AI, WhatsApp, payments, credits, or document processing yet.
```

---

## Product Principle

Build the smallest trusted utility that makes users say:

**“Finally, I understand this document.”**
