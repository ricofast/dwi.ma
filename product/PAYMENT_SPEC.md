# dwi.ma Payment Specification

Payment provider for MVP: **Digital Virgo**

The payment system should be built as a provider abstraction so other providers can be added later.

---

## 1. Payment Model

dwi.ma uses credits.

Users spend credits to:

- Explain a document.
- Explain pasted text.
- Generate a professional message.
- Transcribe and generate from voice input.

Payments buy credit packages.

---

## 2. Initial Product Packages

| Code | Name | Price | Credits |
|---|---|---:|---:|
| FREE_TRIAL | Free trial | 0 MAD | 3 |
| DOC_1 | One document | 5 MAD | 1 |
| MINI_10 | Mini pack | 19 MAD | 10 |
| PRO_30 | Pro pack | 49 MAD | 30 |
| SME_100 | SME pack | 99 MAD | 100 |

---

## 3. Credit Consumption

| Action | Credits |
|---|---:|
| Explain pasted text | 1 |
| Explain document | 1 |
| Generate message from text | 1 |
| Transcribe + generate from voice | 1 or 2 |
| Send result to WhatsApp | 0 initially |

Decision to finalize later: whether voice should cost 1 or 2 credits depending on transcription cost.

---

## 4. Payment Flow

```text
User selects package
  |
  v
Backend creates PaymentTransaction(status=pending)
  |
  v
Backend calls Digital Virgo API
  |
  v
User completes payment
  |
  v
Digital Virgo sends callback
  |
  v
Backend verifies callback
  |
  v
Transaction marked paid
  |
  v
Credits added to wallet
  |
  v
User notified in PWA/WhatsApp
```

---

## 5. Required Models

### PaymentProduct

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

### PaymentTransaction

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
- `updated_at`
- `paid_at`

Statuses:

- `pending`
- `paid`
- `failed`
- `cancelled`
- `refunded`

### PaymentWebhookEvent

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

## 6. API Endpoints

### GET /api/payments/products

Returns active packages.

### POST /api/payments/start

Input:

```json
{
  "product_code": "MINI_10",
  "phone_number": "+2126XXXXXXXX"
}
```

Output:

```json
{
  "transaction_id": "uuid",
  "payment_url": "string",
  "status": "pending"
}
```

### POST /api/payments/digital-virgo/callback

Receives provider callback.

Output:

```json
{
  "status": "ok"
}
```

---

## 7. Idempotency Rules

Payment callback must be idempotent.

Rules:

1. If transaction is already paid, do not add credits again.
2. If provider transaction ID already exists as paid, ignore duplicate.
3. Use database transaction/locking when updating wallet.
4. Store all raw callbacks.
5. Unique index should be added on provider transaction ID when available.

---

## 8. Wallet Credit Activation

When payment is verified successful:

1. Mark transaction as paid.
2. Add credits to wallet.
3. Create CreditAdjustment.
4. Send notification.
5. Store audit log.

Do not add credits if:

- Signature invalid.
- Transaction not found.
- Transaction amount mismatch.
- Product mismatch.
- Transaction already paid.
- Provider status is failed/cancelled.

---

## 9. Provider Abstraction

Create:

```text
apps/payments/services/
  base.py
  digital_virgo.py
  wallet_crediting.py
```

Suggested interface:

```python
class PaymentProvider:
    def create_payment(self, transaction): ...
    def verify_callback(self, request): ...
    def parse_callback(self, payload): ...
```

---

## 10. Digital Virgo TODOs

Exact implementation depends on Digital Virgo contract/docs.

Codex should create placeholders for:

- API base URL.
- Merchant ID.
- API key.
- Webhook secret.
- Signature verification.
- Callback schema parsing.
- Payment URL creation.

Do not invent undocumented Digital Virgo fields.

Use clearly marked TODOs where provider documentation is required.

---

## 11. Payment Failure Handling

If payment fails:

- Mark transaction failed.
- Do not add credits.
- Show failure page.
- Offer retry.
- Send WhatsApp failure message if applicable.

Message:

```text
ما كملش الأداء.
جرب مرة أخرى أو اختار عرض آخر.
```

---

## 12. Payment Success Message

```text
تم الأداء بنجاح ✅
تزادو ليك {{credits_added}} كريدي.
الرصيد الحالي ديالك: {{new_balance}}.
```

---

## 13. Tests Required

- Start payment creates pending transaction.
- Unknown product fails.
- Successful callback marks transaction paid.
- Successful callback adds correct credits.
- Duplicate callback does not double-credit.
- Failed callback does not add credits.
- Invalid signature does not add credits.
