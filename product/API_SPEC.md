# dwi.ma API Specification

This document defines the initial Django Ninja API endpoints for the MVP.

Base path:

```text
/api/
```

---

## 1. Auth and Profile

### GET /api/me

Returns current user profile and wallet.

Response:

```json
{
  "id": "uuid",
  "phone_number": "+2126XXXXXXXX",
  "full_name": "string",
  "preferred_language": "darija_arabic",
  "whatsapp_opt_in": true,
  "credits_balance": 3
}
```

---

### POST /api/auth/start

Starts a phone-based authentication flow.

Input:

```json
{
  "phone_number": "+2126XXXXXXXX"
}
```

Response:

```json
{
  "status": "otp_sent_or_stubbed",
  "phone_number": "+2126XXXXXXXX"
}
```

MVP note: OTP can be stubbed in local development.

---

### POST /api/auth/verify

Verifies OTP.

Input:

```json
{
  "phone_number": "+2126XXXXXXXX",
  "otp": "123456"
}
```

Response:

```json
{
  "status": "authenticated",
  "user_id": "uuid"
}
```

---

## 2. Documents

### POST /api/documents/upload

Uploads a PDF or image.

Request:

- Multipart form data
- `file`
- `consent_accepted=true`
- `source=pwa`

Response:

```json
{
  "document_id": "uuid",
  "status": "uploaded"
}
```

Validation:

- Allowed: PDF, JPG, JPEG, PNG, WEBP.
- Max size from `DOCUMENT_MAX_UPLOAD_MB`.
- Consent must be accepted.

---

### POST /api/documents/{document_id}/explain

Creates document explanation job.

Input:

```json
{
  "output_language": "darija_arabic",
  "send_to_whatsapp": false
}
```

Response:

```json
{
  "job_id": "uuid",
  "status": "queued"
}
```

Rules:

- Check wallet balance.
- Do not charge credit yet.
- Queue Celery task.

---

### GET /api/documents/{document_id}/analysis

Returns document analysis if complete.

Response:

```json
{
  "status": "completed",
  "document_type": "administrative_form",
  "short_summary_darija": "string",
  "important_points_darija": ["string"],
  "extracted_entities": {
    "names": ["string"],
    "dates": ["string"],
    "amounts": ["string"],
    "deadlines": ["string"],
    "obligations": ["string"]
  },
  "unclear_points_darija": ["string"],
  "next_steps_darija": ["string"],
  "disclaimer_darija": "string",
  "full_answer_darija": "string"
}
```

If not completed:

```json
{
  "status": "processing"
}
```

---

### DELETE /api/documents/{document_id}

Deletes the physical file and marks document deleted.

Response:

```json
{
  "status": "deleted"
}
```

---

## 3. Text Explanation

### POST /api/assistant/explain-text

Input:

```json
{
  "text": "string",
  "output_language": "darija_arabic",
  "send_to_whatsapp": false
}
```

Response:

```json
{
  "job_id": "uuid",
  "status": "queued"
}
```

Rules:

- Validate text length.
- Check credits.
- Queue AI job.
- Charge credit only after success.

---

## 4. Audio and Message Generation

### POST /api/audio/upload

Uploads audio file.

Request:

- Multipart form data
- `file`
- `source=pwa`

Response:

```json
{
  "voice_note_id": "uuid",
  "status": "uploaded"
}
```

---

### POST /api/audio/{voice_note_id}/transcribe

Creates transcription job.

Response:

```json
{
  "job_id": "uuid",
  "status": "queued"
}
```

---

### POST /api/assistant/generate-message

Generates professional message from text or transcript.

Input:

```json
{
  "input_text": "bghit nsendi message l fournisseur...",
  "target_format": "professional_french_email",
  "tone": "polite_firm"
}
```

Allowed `target_format`:

- `professional_french_email`
- `professional_arabic_message`
- `polished_darija_whatsapp`
- `short_reply`

Allowed `tone`:

- `polite`
- `polite_firm`
- `friendly`
- `formal`
- `short`

Response:

```json
{
  "job_id": "uuid",
  "status": "queued"
}
```

---

## 5. AI Jobs

### GET /api/jobs/{job_id}

Returns job status and result.

Response if processing:

```json
{
  "job_id": "uuid",
  "status": "running"
}
```

Response if completed:

```json
{
  "job_id": "uuid",
  "status": "completed",
  "result_text": "string",
  "result_json": {}
}
```

Response if failed:

```json
{
  "job_id": "uuid",
  "status": "failed",
  "error_message": "string"
}
```

---

### POST /api/jobs/{job_id}/feedback

Input:

```json
{
  "rating": "helpful",
  "comment": "string"
}
```

Allowed ratings:

- `helpful`
- `unclear`
- `wrong`
- `dangerous`

Response:

```json
{
  "status": "saved"
}
```

---

## 6. WhatsApp

### GET /api/whatsapp/webhook

Webhook verification endpoint.

Query params depend on WhatsApp verification challenge.

Response:

```text
challenge
```

---

### POST /api/whatsapp/webhook

Receives WhatsApp webhook events.

Rules:

1. Validate signature if configured.
2. Store raw payload.
3. Return 200 quickly.
4. Queue Celery processing.

Response:

```json
{
  "status": "received"
}
```

---

### POST /api/whatsapp/send-result

Sends completed job result to WhatsApp.

Input:

```json
{
  "job_id": "uuid",
  "phone_number": "+2126XXXXXXXX"
}
```

Response:

```json
{
  "status": "queued_or_sent"
}
```

---

## 7. Wallet

### GET /api/wallet

Response:

```json
{
  "balance": 3,
  "total_purchased": 0,
  "total_used": 0
}
```

---

### GET /api/wallet/usage

Response:

```json
{
  "items": [
    {
      "event_type": "document_explanation",
      "credits_charged": 1,
      "status": "charged",
      "created_at": "datetime"
    }
  ]
}
```

---

## 8. Payments

### GET /api/payments/products

Response:

```json
{
  "products": [
    {
      "code": "DOC_1",
      "name": "One document",
      "price_mad": 5,
      "credits": 1
    }
  ]
}
```

---

### POST /api/payments/start

Input:

```json
{
  "product_code": "MINI_10",
  "phone_number": "+2126XXXXXXXX"
}
```

Response:

```json
{
  "transaction_id": "uuid",
  "payment_url": "https://provider-payment-url",
  "status": "pending"
}
```

---

### POST /api/payments/digital-virgo/callback

Receives Digital Virgo callback.

Rules:

- Store raw callback.
- Verify signature.
- Find transaction.
- Check idempotency.
- Mark paid if successful.
- Add credits.
- Notify user.

Response:

```json
{
  "status": "ok"
}
```

---

## 9. Admin-Oriented API Later

Not required for first MVP if Django admin is sufficient.

Potential future endpoints:

- `/api/admin/jobs`
- `/api/admin/payments`
- `/api/admin/users/{id}/credits/adjust`
- `/api/admin/documents/{id}/retry`
