# dwi.ma Development Milestones

Use these milestones one at a time. Do not ask Codex to build the full app in one pass.

---

## Milestone 1 — Project Foundation

### Goal

Create the base Django project.

### Deliverables

- Django 5 project.
- Python 3.12+ support.
- PostgreSQL configuration.
- Django Ninja installed and configured.
- Celery + Redis configured.
- Environment-based settings.
- Required apps created.
- Custom user model using phone number.
- Bootstrap 5 base template.
- Basic dashboard page.
- Django admin enabled.
- `.env.example`.
- README setup instructions.
- Basic tests.

### Do not implement

- AI.
- WhatsApp.
- Payments.
- Credits.
- Document processing.

### Codex prompt

```text
Implement Milestone 1 only: Django project foundation.

Requirements:
- Django 5 project
- Python 3.12+
- PostgreSQL support
- Django Ninja installed and configured
- Celery + Redis configured
- Environment-based settings
- Custom user model using phone number as main identity field
- Apps created:
  - accounts
  - wallet
  - payments
  - whatsapp
  - documents
  - audio
  - assistant
  - notifications
  - core
- Bootstrap 5 base template
- Basic dashboard page
- Django admin setup
- .env.example
- README with setup steps
- Basic tests confirming project loads and custom user works

Do not implement AI, WhatsApp, payments, credits, or document processing yet.
```

---

## Milestone 2 — Wallet and Credits

### Goal

Implement the credit system.

### Deliverables

- CreditWallet model.
- UsageEvent model.
- CreditAdjustment model.
- Free credits on signup.
- Wallet service functions.
- Admin integration.
- Tests.

### Codex prompt

```text
Implement Milestone 2 only: wallet and credits.

Create CreditWallet, UsageEvent, and CreditAdjustment models.
Add services to:
- grant free credits
- check balance
- reserve credits if needed
- charge credits
- refund credits
- manually adjust credits

Rules:
- Failed jobs must not consume credits.
- Use database transactions.
- Add tests for wallet operations.
Do not implement payments yet.
```

---

## Milestone 3 — Document Upload and Extraction

### Goal

Allow users to upload documents and extract text from simple PDFs.

### Deliverables

- UploadedDocument model.
- ExtractedText model.
- Upload page.
- Upload API.
- File validation.
- Text extraction for text PDFs.
- Status transitions.
- Tests.

### Codex prompt

```text
Implement Milestone 3 only: document upload and text extraction.

Requirements:
- Accept PDF, JPG, JPEG, PNG, WEBP.
- Enforce max file size from settings.
- Require document processing consent.
- Create UploadedDocument and ExtractedText models.
- Add upload form and API endpoint.
- Extract text from text-based PDFs using PyMuPDF or pdfplumber.
- Store extraction method.
- Add status transitions.
- Add tests.

Do not implement LLM explanation yet.
```

---

## Milestone 4 — AI Document Explanation

### Goal

Generate Darija explanation for uploaded documents.

### Deliverables

- AIJob model.
- Prompt service.
- AI provider abstraction.
- Mock AI provider for tests.
- Real provider placeholder.
- DocumentAnalysis model.
- Celery task.
- Result page.
- JSON parsing and retry.
- Tests.

### Codex prompt

```text
Implement Milestone 4 only: AI document explanation.

Requirements:
- Create AIJob and DocumentAnalysis models.
- Add AI provider abstraction with mock provider for tests.
- Add real provider placeholder for OpenAI/Anthropic.
- Implement document explanation prompt from product/PROMPTS.md.
- Run explanation in Celery task.
- Return structured JSON.
- Retry once if JSON is invalid.
- Save result.
- Charge credit only after successful completion.
- Failed job must not charge credit.
- Add result detail page.
- Add tests.
```

---

## Milestone 5 — Pasted Text Explanation

### Goal

Allow users to paste text and receive Darija explanation.

### Deliverables

- Text explanation page.
- API endpoint.
- AI job creation.
- Result page reuse.
- Credit charging.
- Tests.

### Codex prompt

```text
Implement Milestone 5 only: pasted text explanation.

Requirements:
- Add page for pasted text.
- Add API endpoint /api/assistant/explain-text.
- Validate text length.
- Use prompt from product/PROMPTS.md.
- Run in Celery.
- Save AIJob result.
- Charge credit only after success.
- Reuse result page.
- Add tests.
```

---

## Milestone 6 — WhatsApp Companion

### Goal

Integrate WhatsApp webhook and outbound messages.

### Deliverables

- Webhook verification.
- Inbound webhook storage.
- Inbound message model.
- Outbound message model.
- Send text service.
- Main menu.
- Send result to WhatsApp.
- Tests.

### Codex prompt

```text
Implement Milestone 6 only: WhatsApp companion.

Requirements:
- Implement WhatsApp webhook verification endpoint.
- Implement inbound webhook POST endpoint.
- Store raw webhook payload.
- Return 200 quickly.
- Queue Celery processing task.
- Store inbound messages.
- Add outbound message send service.
- Add simple menu message.
- Add send-result-to-WhatsApp endpoint.
- Add tests.

Do not build a generic chatbot.
```

---

## Milestone 7 — Voice Transcription and Message Generation

### Goal

Support audio input and Darija-to-professional-message generation.

### Deliverables

- VoiceNote model.
- TranscriptionJob model.
- Audio upload.
- Transcription provider abstraction.
- Message generation prompt.
- Result page.
- Tests.

### Codex prompt

```text
Implement Milestone 7 only: voice transcription and message generation.

Requirements:
- Add audio upload.
- Create VoiceNote and TranscriptionJob models.
- Add transcription service abstraction.
- Add mock transcription provider for tests.
- Add OpenAI provider placeholder.
- Add message generation flow.
- Support target formats:
  - professional_french_email
  - professional_arabic_message
  - polished_darija_whatsapp
  - short_reply
- Charge credits only after success.
- Add tests.
```

---

## Milestone 8 — Digital Virgo Payments

### Goal

Implement payment skeleton and credit activation.

### Deliverables

- PaymentProduct model.
- PaymentTransaction model.
- PaymentWebhookEvent model.
- Products endpoint.
- Start payment endpoint.
- Callback endpoint.
- Idempotent credit activation.
- Tests.

### Codex prompt

```text
Implement Milestone 8 only: Digital Virgo payment skeleton.

Requirements:
- Add PaymentProduct, PaymentTransaction, PaymentWebhookEvent models.
- Add initial credit packages.
- Add /api/payments/products endpoint.
- Add /api/payments/start endpoint.
- Add /api/payments/digital-virgo/callback endpoint.
- Keep provider logic isolated.
- Add signature verification placeholder with TODO.
- Store raw callback payloads.
- Ensure duplicate callbacks do not double-credit.
- Add tests.
```

---

## Milestone 9 — Privacy, Admin, and Polish

### Goal

Add trust and operational controls.

### Deliverables

- ConsentLog.
- Delete document.
- AuditLog.
- User feedback.
- Admin retry.
- Admin credit refund.
- Privacy and terms pages.
- Tests.

### Codex prompt

```text
Implement Milestone 9 only: privacy, admin, and polish.

Requirements:
- Add ConsentLog if not already implemented.
- Add document deletion service.
- Add AuditLog.
- Add user feedback buttons for AI results.
- Add admin actions:
  - retry failed AI job
  - refund credits
  - delete document
- Add privacy policy and terms pages.
- Add tests for deletion, consent logging, and admin actions.
```
