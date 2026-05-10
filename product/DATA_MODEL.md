# dwi.ma Data Model

This document describes the initial data model for the MVP.

Use UUID primary keys for externally referenced objects where practical.

---

## 1. accounts.User

Custom user model.

Fields:

- `id`
- `phone_number`
- `email`
- `full_name`
- `is_active`
- `is_staff`
- `is_superuser`
- `date_joined`
- `last_login`

Notes:

- Phone number is the main identity field.
- Email is optional.

---

## 2. accounts.Profile

Fields:

- `id`
- `user`
- `preferred_language`
- `preferred_output_channel`
- `whatsapp_opt_in`
- `onboarding_completed`
- `created_at`
- `updated_at`

Allowed preferred language:

- `darija_arabic`
- `darija_latin`
- `french`
- `arabic`

Allowed output channel:

- `web`
- `whatsapp`

---

## 3. accounts.ConsentLog

Fields:

- `id`
- `user`
- `phone_number`
- `consent_type`
- `consent_text_version`
- `ip_address`
- `user_agent`
- `created_at`

Consent types:

- `privacy_policy`
- `document_processing`
- `whatsapp_optin`
- `marketing`

---

## 4. wallet.CreditWallet

Fields:

- `id`
- `user`
- `balance`
- `total_purchased`
- `total_used`
- `created_at`
- `updated_at`

---

## 5. wallet.UsageEvent

Fields:

- `id`
- `user`
- `ai_job`
- `event_type`
- `credits_charged`
- `status`
- `created_at`

Event types:

- `document_explanation`
- `text_explanation`
- `voice_transcription`
- `message_generation`

Statuses:

- `reserved`
- `charged`
- `refunded`
- `failed`

---

## 6. wallet.CreditAdjustment

Fields:

- `id`
- `user`
- `amount`
- `reason`
- `created_by`
- `created_at`

---

## 7. documents.UploadedDocument

Fields:

- `id`
- `user`
- `original_filename`
- `file`
- `file_type`
- `file_size`
- `sha256_hash`
- `status`
- `source`
- `whatsapp_media_id`
- `deleted_at`
- `created_at`
- `updated_at`

Statuses:

- `uploaded`
- `extracting`
- `processing`
- `completed`
- `failed`
- `deleted`

Sources:

- `pwa`
- `whatsapp`

---

## 8. documents.ExtractedText

Fields:

- `id`
- `document`
- `extraction_method`
- `text`
- `confidence`
- `page_count`
- `created_at`

Extraction methods:

- `pypdf`
- `pymupdf`
- `pdfplumber`
- `ocr`
- `vision_llm`

---

## 9. documents.DocumentAnalysis

Fields:

- `id`
- `document`
- `ai_job`
- `document_type`
- `summary_darija`
- `important_points_json`
- `extracted_entities_json`
- `unclear_points_json`
- `next_steps_darija`
- `disclaimer_darija`
- `full_response_text`
- `created_at`

---

## 10. audio.VoiceNote

Fields:

- `id`
- `user`
- `audio_file`
- `source`
- `whatsapp_media_id`
- `duration_seconds`
- `status`
- `created_at`

Sources:

- `pwa`
- `whatsapp`

Statuses:

- `uploaded`
- `transcribing`
- `completed`
- `failed`
- `deleted`

---

## 11. audio.TranscriptionJob

Fields:

- `id`
- `voice_note`
- `provider`
- `model`
- `transcript`
- `language_detected`
- `confidence`
- `status`
- `error_message`
- `created_at`
- `completed_at`

---

## 12. assistant.AIJob

Fields:

- `id`
- `user`
- `job_type`
- `provider`
- `model`
- `input_hash`
- `input_preview`
- `prompt_version`
- `status`
- `result_json`
- `result_text`
- `error_message`
- `cost_estimate`
- `latency_ms`
- `created_at`
- `completed_at`

Job types:

- `document_explanation`
- `text_explanation`
- `message_generation`
- `intent_detection`

Statuses:

- `queued`
- `running`
- `completed`
- `failed`

---

## 13. assistant.UserFeedback

Fields:

- `id`
- `user`
- `ai_job`
- `rating`
- `comment`
- `created_at`

Ratings:

- `helpful`
- `unclear`
- `wrong`
- `dangerous`

---

## 14. whatsapp.WhatsAppWebhookEvent

Fields:

- `id`
- `event_id`
- `payload_json`
- `processed`
- `received_at`
- `processed_at`
- `error_message`

---

## 15. whatsapp.WhatsAppInboundMessage

Fields:

- `id`
- `user`
- `wa_id`
- `message_id`
- `message_type`
- `text_body`
- `media_id`
- `payload_json`
- `created_at`

Message types:

- `text`
- `audio`
- `image`
- `document`
- `interactive`

---

## 16. whatsapp.WhatsAppOutboundMessage

Fields:

- `id`
- `user`
- `wa_id`
- `message_id`
- `message_type`
- `text_body`
- `template_name`
- `status`
- `payload_json`
- `created_at`
- `updated_at`

Statuses:

- `queued`
- `sent`
- `delivered`
- `read`
- `failed`

---

## 17. payments.PaymentProduct

Fields:

- `id`
- `code`
- `name`
- `description`
- `price_mad`
- `credits`
- `active`
- `created_at`
- `updated_at`

---

## 18. payments.PaymentTransaction

Fields:

- `id`
- `user`
- `provider`
- `provider_transaction_id`
- `product`
- `amount_mad`
- `currency`
- `status`
- `raw_request_json`
- `raw_response_json`
- `created_at`
- `paid_at`

Statuses:

- `pending`
- `paid`
- `failed`
- `cancelled`
- `refunded`

---

## 19. payments.PaymentWebhookEvent

Fields:

- `id`
- `provider`
- `provider_event_id`
- `payload_json`
- `processed`
- `created_at`
- `processed_at`
- `error_message`

---

## 20. core.AuditLog

Fields:

- `id`
- `actor`
- `action`
- `target_type`
- `target_id`
- `metadata_json`
- `created_at`
