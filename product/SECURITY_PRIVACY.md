# dwi.ma Security and Privacy Requirements

dwi.ma processes documents, images, voice notes, and messages that may contain sensitive personal information.

Security and privacy must be designed from the beginning.

---

## 1. Core Privacy Principles

1. Ask for user consent before document processing.
2. Do not use user documents for model training by default.
3. Store original files only as long as necessary.
4. Allow users to delete uploaded documents.
5. Keep files private.
6. Log sensitive operations.
7. Add clear disclaimers for high-risk document types.

---

## 2. Data Types

dwi.ma may process:

- Names.
- Phone numbers.
- Email addresses.
- Identity-related documents.
- Bank documents.
- Telecom bills.
- Contracts.
- Invoices.
- Administrative forms.
- Medical-looking documents.
- Voice notes.
- WhatsApp messages.

Treat uploaded files and extracted text as sensitive.

---

## 3. Consent Requirements

Before processing a document, user must accept:

```text
كنوافق أن dwi.ma يعالج هاد الوثيقة باش يشرحها ليا.
عارف أن هاد الخدمة غير للمساعدة وماشي استشارة قانونية أو طبية أو مالية رسمية.
```

Store:

- user
- consent type
- consent version
- timestamp
- IP address if available
- user agent if available

Consent types:

- `privacy_policy`
- `document_processing`
- `whatsapp_optin`
- `marketing`

---

## 4. File Storage

### Local development

Files can be stored locally under `media/`.

### Production

Use private S3-compatible object storage.

Rules:

- No public file URLs.
- Use signed URLs only if needed.
- Validate file type.
- Enforce file size.
- Store hash of file.
- Support deletion.

---

## 5. Document Deletion

User must be able to delete uploaded document.

Deletion should:

1. Delete physical file.
2. Mark UploadedDocument as deleted.
3. Set `deleted_at`.
4. Keep minimal audit metadata.
5. Optionally delete extracted text depending on retention setting.

Do not silently keep original file after user deletion.

---

## 6. Retention Policy

Initial suggested retention:

- Original uploaded files: 30 days by default.
- Extracted text: kept with result unless user deletes.
- AI results: kept in user history unless deleted.
- Payment records: kept for business/accounting needs.
- Raw WhatsApp payloads: keep for limited debugging period.

Create system setting:

```text
ORIGINAL_FILE_RETENTION_DAYS=30
```

---

## 7. AI Provider Privacy

When sending content to OpenAI/Anthropic/etc.:

- Send only what is needed.
- Avoid sending unnecessary metadata.
- Do not send payment data to AI.
- Do not send secrets.
- Do not send full user profile unless needed.

Add future option:

```text
Do not store my document after processing.
```

---

## 8. Security Requirements

### Secrets

Store all secrets in environment variables:

- Django secret key.
- Database URL.
- Redis URL.
- OpenAI key.
- Anthropic key.
- WhatsApp token.
- Digital Virgo key.
- Storage credentials.

Never commit secrets.

### Upload validation

Validate:

- MIME type.
- File extension.
- File size.
- Empty files.
- Suspicious files.

Allowed extensions:

- `.pdf`
- `.jpg`
- `.jpeg`
- `.png`
- `.webp`

### Webhook validation

Validate when credentials are available:

- WhatsApp signature.
- Digital Virgo callback signature.

### Admin security

- Use strong admin passwords.
- Limit admin access.
- Do not expose admin publicly without protection.
- Log admin actions.

---

## 9. Disclaimers

For legal, medical, financial, banking, insurance, tax, employment, contract, or administrative documents, include:

```text
ملاحظة: هاد الشرح غير باش يعاونك تفهم الوثيقة، وماشي استشارة قانونية أو طبية أو مالية أو إدارية رسمية.
```

The assistant must not:

- Diagnose medical conditions.
- Recommend treatment.
- Give legal conclusions.
- Tell user to ignore professional advice.
- Give tax/accounting decisions.
- Invent missing obligations.

---

## 10. Audit Logs

Audit these events:

- Document uploaded.
- Document deleted.
- Credits manually adjusted.
- Payment callback processed.
- Admin retry job.
- Admin refund credits.
- User consent accepted.

AuditLog fields:

- actor
- action
- target_type
- target_id
- metadata_json
- created_at

---

## 11. Abuse and Rate Limits

Add basic limits:

- Max upload size.
- Max number of free tasks per user.
- Max failed attempts per hour.
- Max WhatsApp messages per user per hour.

Future:

- IP rate limiting.
- Phone-number rate limiting.
- Abuse detection.
- Blocklist.

---

## 12. Tests Required

- Consent is required for document upload.
- File size validation works.
- Invalid file type rejected.
- Deleted document removes physical file.
- Sensitive category adds disclaimer.
- Failed job does not charge credits.
- Payment callback cannot double-credit.
