## Milestone 1 — Project Foundation

Goal:
Create the Django project foundation for dwi.ma.

Requirements:
- Django 5 project
- Python 3.12+
- PostgreSQL support
- Django Ninja installed and configured
- Celery + Redis configured
- Environment-based settings
- Custom user model using phone number as the main identity field
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
- Basic Django admin setup
- .env.example
- README with setup steps
- Basic tests confirming project loads and custom user works

Do not implement:
- AI
- WhatsApp
- payments
- document processing
- credits yet

After implementation:
- Show the files changed.
- Explain how to run the project.
- Explain how to run tests.


Read AGENTS.md and the product documentation, especially:

- product/PRD.md
- product/DATA_MODEL.md
- product/MILESTONES.md

## Milestone 2 — Wallet and Credits

Implement Milestone 2 only: Wallet and Credits.

Goal:
Create the credit system that controls usage of dwi.ma. Users should receive free credits, spend credits only when an AI job succeeds, and never lose credits when a job fails.

Requirements:

1. Models
Create or complete the following models in the wallet app:

- CreditWallet
  - user
  - balance
  - total_purchased
  - total_used
  - created_at
  - updated_at

- UsageEvent
  - user
  - event_type
  - credits
  - status: reserved, charged, refunded, failed
  - reference_type optional
  - reference_id optional
  - metadata JSON field
  - created_at
  - updated_at

- CreditAdjustment
  - user
  - amount
  - reason
  - created_by optional
  - metadata JSON field
  - created_at

2. Wallet creation
- Automatically create a CreditWallet when a new user is created.
- Grant default free credits to new users.
- Read the default number of free credits from settings or environment variable:
  DEFAULT_FREE_CREDITS=3

3. Wallet service layer
Create a wallet service module, for example:

apps/wallet/services.py

Implement clean service functions:

- get_wallet(user)
- get_balance(user)
- grant_free_credits(user)
- add_credits(user, amount, reason, metadata=None)
- reserve_credits(user, amount, event_type, reference_type=None, reference_id=None, metadata=None)
- charge_reserved_usage(usage_event)
- refund_usage(usage_event, reason=None)
- fail_usage(usage_event, reason=None)
- can_spend(user, amount)

Important:
- Do not allow negative balances.
- Use database transactions where needed.
- Use select_for_update where appropriate to prevent race conditions.
- Charging should only happen when a reserved usage event is completed successfully.
- Failed jobs must not consume credits.
- Refunds must restore credits only if the usage was already charged.

4. API endpoints
Add Django Ninja endpoints for wallet:

- GET /api/wallet/
  Returns current user wallet balance and totals.

- GET /api/wallet/usage/
  Returns recent usage events for the current user.

- POST /api/wallet/admin-adjust/
  Staff-only endpoint to manually add or remove credits.

If authentication is not fully implemented yet, use the existing project auth pattern from Milestone 1 and keep the endpoint structure ready.

5. Django admin
Register wallet models in Django admin:
- CreditWallet
- UsageEvent
- CreditAdjustment

Admin should show:
- user
- balance
- totals
- event status
- created_at
- updated_at

6. Tests
Add tests for:

- Wallet is created automatically for a new user.
- New user receives DEFAULT_FREE_CREDITS.
- can_spend returns true when balance is enough.
- can_spend returns false when balance is insufficient.
- reserve_credits creates a reserved UsageEvent.
- charge_reserved_usage deducts credits.
- fail_usage does not deduct credits.
- refund_usage restores credits after charge.
- Duplicate charging of the same UsageEvent is prevented.
- Balance cannot go below zero.
- Staff adjustment can add credits.
- Staff adjustment can remove credits only if sufficient balance exists.

7. Constraints
- Do not implement AI.
- Do not implement WhatsApp.
- Do not implement Digital Virgo payments.
- Do not implement document processing.
- Do not add future features.
- Keep this milestone focused only on wallet, credits, usage events, services, admin, and tests.

8. After implementation
Show:
- Files changed
- New models
- New service functions
- New API endpoints
- How to run migrations
- How to run tests

## Milestone 3 — Document Upload and Extraction
Read AGENTS.md and the product documentation, especially:

- product/PRD.md
- product/DATA_MODEL.md
- product/API_SPEC.md
- product/MILESTONES.md
- product/SECURITY_PRIVACY.md

Implement Milestone 3 only: Document Upload and Basic Text Extraction.

Goal:
Allow users to upload PDF/image documents, validate them, store them securely, and extract text from text-based PDFs. This milestone does NOT call any LLM yet. AI document explanation will be implemented in Milestone 4.

Requirements:

1. Models

Create or complete the following models in the documents app.

UploadedDocument:
- id: UUID primary key
- user: ForeignKey to User
- original_filename
- file
- file_type
- file_size
- sha256_hash
- source: choices = pwa, whatsapp, admin
- status: choices = uploaded, extracting, extracted, extraction_failed, processing, completed, failed, deleted
- extraction_error nullable
- deleted_at nullable
- created_at
- updated_at

ExtractedText:
- id: UUID primary key
- document: OneToOneField or ForeignKey to UploadedDocument
- extraction_method: choices = pymupdf, pdfplumber, pypdf, ocr, vision_llm, manual
- text
- page_count nullable
- confidence nullable
- metadata JSON field
- created_at
- updated_at

2. File validation

Accept only:
- PDF
- JPG
- JPEG
- PNG
- WEBP

Add settings:
- DOCUMENT_MAX_UPLOAD_MB=10
- ALLOWED_DOCUMENT_EXTENSIONS=pdf,jpg,jpeg,png,webp

Validation rules:
- Reject files larger than DOCUMENT_MAX_UPLOAD_MB.
- Reject unsupported file extensions.
- Reject empty files.
- Save original filename.
- Calculate SHA256 hash.
- Store file size.
- Detect file type from extension and/or content type.
- Do not expose uploaded files publicly.

3. Text extraction service

Create a service module:

apps/documents/services/extraction.py

Implement:

- calculate_file_hash(file)
- validate_document_file(file)
- classify_document_file(uploaded_document)
- extract_text_from_pdf(uploaded_document)
- extract_text(uploaded_document)

For this milestone:
- Implement text extraction only for text-based PDFs.
- Use PyMuPDF if available, otherwise use pdfplumber.
- If PDF has no extractable text, mark extraction as extraction_failed with a clear message:
  "No extractable text found. Scanned document support will be added later."
- For image files, do not perform OCR yet. Mark extraction as extraction_failed with:
  "Image OCR support will be added in a later milestone."
- Do not call Claude, OpenAI, OCR, or any vision model yet.

4. Upload flow in PWA

Create mobile-first Bootstrap 5 templates:

- documents/upload.html
- documents/detail.html
- documents/extraction_result.html

User flow:
1. User opens “شرح ليا وثيقة”.
2. User sees a privacy/consent notice.
3. User uploads PDF/image.
4. System validates and saves document.
5. System starts extraction.
6. User sees extraction status/result.
7. If extraction succeeds, show extracted text preview.
8. If extraction fails, show friendly message.

Important:
- Keep UI simple and mobile-first.
- Use Darija labels where appropriate.
- Do not show technical errors to the user.
- Technical errors should be logged and stored in extraction_error.

5. API endpoints using Django Ninja

Add endpoints:

POST /api/documents/upload
- Multipart upload
- Requires consent_accepted=true
- Returns document_id, status, filename, file_type, file_size

GET /api/documents/{document_id}
- Returns document metadata and status

POST /api/documents/{document_id}/extract
- Starts text extraction synchronously or through Celery depending on existing project setup
- Returns extraction status

GET /api/documents/{document_id}/extracted-text
- Returns extracted text if available

DELETE /api/documents/{document_id}
- Deletes or marks document as deleted
- If physical file deletion is already supported, delete the file too
- Otherwise mark deleted_at and status=deleted

6. Celery task

If Celery is already configured from Milestone 1, add:

apps/documents/tasks.py

Task:
- extract_document_text_task(document_id)

Behavior:
- Set status to extracting
- Run extraction
- Save ExtractedText if successful
- Set status to extracted
- If failure, set status to extraction_failed
- Store extraction_error
- Never charge credits in this milestone

7. Admin

Register:

- UploadedDocument
- ExtractedText

Admin should show:
- user
- original_filename
- file_type
- file_size
- status
- source
- created_at
- updated_at
- deleted_at

Add filters:
- status
- file_type
- source
- created_at

8. Tests

Add tests for:

- PDF upload succeeds.
- Image upload succeeds but extraction is marked unsupported for now.
- Unsupported extension is rejected.
- File larger than max size is rejected.
- Empty file is rejected.
- SHA256 hash is calculated.
- UploadedDocument is created with correct metadata.
- Text-based PDF extraction succeeds.
- Scanned/image-only PDF extraction fails gracefully if no text is found.
- Image OCR returns friendly unsupported message for now.
- Delete endpoint marks document as deleted.
- User cannot access another user’s document.
- Extraction failure does not affect wallet credits.
- API returns expected status codes.

9. Constraints

Do not implement:
- AI document explanation.
- Claude/OpenAI document analysis.
- OCR for images.
- WhatsApp media upload.
- Digital Virgo payments.
- Advanced document classification.
- Credit deduction.
- Voice transcription.

This milestone is only about:
- Uploading documents.
- Validating documents.
- Storing documents.
- Extracting text from text-based PDFs.
- Showing extraction results.

10. After implementation

Show:
- Files changed
- New models
- New services
- New API endpoints
- New templates
- New tests
- How to run migrations
- How to run document tests

## Milestone 4 — AI Document Explanation
Read AGENTS.md and the product documentation, especially:

- product/PRD.md
- product/DATA_MODEL.md
- product/API_SPEC.md
- product/PROMPTS.md
- product/MILESTONES.md
- product/SECURITY_PRIVACY.md

Implement Milestone 4 only: AI Document Explanation.

Goal:
Take extracted document text from Milestone 3, send it to an LLM using a structured Moroccan Darija document-explanation prompt, save the result, show it to the user, and integrate wallet credit charging safely.

Important:
This milestone does NOT implement WhatsApp, payments, OCR, voice transcription, or generic chatbot features.

Core user story:
As a user, after uploading a document and extracting its text, I can click “شرح ليا الوثيقة”, spend one credit, and receive a structured explanation in simple Moroccan Darija.

Requirements:

1. Models

Create or complete the following models.

In assistant app:

AIJob:
- id: UUID primary key
- user: ForeignKey to User
- job_type: choices = document_explanation, text_explanation, message_generation, intent_detection
- provider
- model
- status: queued, running, completed, failed
- input_hash
- input_preview
- prompt_version
- result_json JSON field nullable
- result_text nullable
- error_message nullable
- cost_estimate nullable
- latency_ms nullable
- created_at
- updated_at
- completed_at nullable

PromptTemplate:
- id
- name
- version
- system_prompt
- user_prompt_template
- output_schema JSON field nullable
- active boolean
- created_at
- updated_at

AIResponse:
- id
- ai_job: OneToOneField or ForeignKey
- raw_response_text
- parsed_json JSON field nullable
- provider_response_id nullable
- created_at

SafetyFlag:
- id
- ai_job
- flag_type: legal, medical, financial, administrative, unclear, hallucination_risk, unsafe
- message
- created_at

In documents app:

DocumentAnalysis:
- id: UUID primary key
- document: ForeignKey or OneToOneField to UploadedDocument
- ai_job: ForeignKey to AIJob
- document_type
- summary_darija
- important_points_json
- extracted_entities_json
- unclear_points_json
- next_steps_json
- disclaimer_darija
- full_response_text
- created_at
- updated_at

2. Prompt template

Create a default active prompt template for document explanation.

System prompt:

You are dwi.ma, a helpful Moroccan Darija assistant.
Your role is to explain documents in simple Moroccan Darija for ordinary Moroccan users.
You must only use information found in the document text.
Do not invent facts.
If something is unclear, say: "هاد النقطة ما واضحةش فهاد الوثيقة."
If the document appears legal, medical, financial, insurance-related, banking-related, administrative, or tax-related, include a short disclaimer that this is only an explanation, not professional advice.
Use simple Moroccan Darija, not formal Arabic.
Keep the answer practical, organized, and easy to read.
Return valid JSON only.

User prompt template:

Explain this document in simple Moroccan Darija.

Document content:
{{document_text}}

Return valid JSON using this exact schema:

{
  "document_type": "string",
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

Rules:
- Return JSON only.
- Do not wrap the JSON in markdown.
- Do not add information that is not in the document.
- If a field has no information, return an empty array or empty string.
- If something is unclear, use: "هاد النقطة ما واضحةش فهاد الوثيقة."

3. AI provider abstraction

Create an AI provider abstraction in:

apps/assistant/services/providers.py

Implement:

- BaseLLMProvider
- MockLLMProvider
- OpenAIProvider placeholder
- AnthropicProvider placeholder
- GeminiProvider placeholder

For this milestone:
- MockLLMProvider must be fully working for tests.
- Real providers can be implemented with environment variables, but must fail gracefully if API keys are missing.
- Provider selection should come from settings:
  DEFAULT_LLM_PROVIDER
  DEFAULT_LLM_MODEL

Service function:

generate_document_explanation(document_text, provider=None, model=None)

It should:
- Load active document explanation prompt.
- Call provider.
- Return raw response text.
- Parse JSON.
- Validate required keys.
- If JSON is invalid, retry once with a JSON repair instruction.
- If still invalid, fail gracefully.

4. Document explanation service

Create:

apps/documents/services/analysis.py

Implement:

explain_document(document_id, user)

Behavior:
1. Load document.
2. Verify document belongs to user.
3. Verify document has ExtractedText.
4. Verify document status is extracted.
5. Check wallet balance.
6. Reserve 1 credit using wallet service.
7. Create AIJob with status queued.
8. Run LLM explanation.
9. Save AIResponse.
10. Save DocumentAnalysis.
11. Set AIJob status completed.
12. Set UploadedDocument status completed.
13. Charge reserved usage.
14. Return DocumentAnalysis.

Failure behavior:
- If no extracted text exists, fail with friendly error.
- If user has insufficient credits, do not create paid job.
- If LLM fails, mark AIJob failed.
- If LLM fails, mark reserved usage as failed and do not deduct credits.
- If JSON parsing fails after retry, mark AIJob failed and do not deduct credits.
- Do not expose raw technical errors to the user.

5. Celery task

Create or complete:

apps/documents/tasks.py

Task:

explain_document_task(document_id, user_id)

Behavior:
- Set AIJob/document status to processing/running.
- Run explanation service.
- Save results.
- Charge credits only on success.
- Fail usage on error.
- Store safe error message.
- Never deduct credits on failed explanation.

6. API endpoints using Django Ninja

Add endpoints:

POST /api/documents/{document_id}/explain

Input:
{
  "output_language": "darija_arabic"
}

Response:
{
  "job_id": "uuid",
  "document_id": "uuid",
  "status": "queued"
}

Rules:
- Requires authenticated user.
- Requires extracted text.
- Requires enough credits.
- Starts Celery task if Celery exists.
- If Celery is not available in local development, support synchronous fallback only if the project already uses that pattern.

GET /api/documents/{document_id}/analysis

Response:
{
  "status": "completed",
  "document_type": "...",
  "summary_darija": "...",
  "important_points": [],
  "extracted_entities": {},
  "unclear_points": [],
  "next_steps": [],
  "disclaimer": "...",
  "full_answer": "..."
}

GET /api/assistant/jobs/{job_id}

Response:
{
  "job_id": "uuid",
  "status": "queued|running|completed|failed",
  "result_available": true/false,
  "error_message": "..."
}

7. PWA templates

Create or update mobile-first Bootstrap templates:

- documents/explain_confirm.html
- documents/processing.html
- documents/analysis_result.html

User flow:
1. User uploads and extracts text.
2. User clicks “شرح ليا الوثيقة”.
3. Confirmation page shows:
   - This will use 1 credit.
   - Current balance.
   - Document filename.
4. User confirms.
5. Processing page polls job status with HTMX.
6. Result page displays structured explanation.

Result page should show:
- Type of document
- Short summary
- Important points
- Names/dates/amounts/deadlines/obligations
- Unclear points
- What to do next
- Disclaimer
- Full answer
- Buttons:
  - Copy result
  - Back to dashboard
  - Delete document

Use simple Darija UI labels where appropriate.

8. Admin

Register:

- AIJob
- PromptTemplate
- AIResponse
- SafetyFlag
- DocumentAnalysis

Admin should show:
- user
- job_type
- provider
- model
- status
- created_at
- completed_at
- error_message

Add filters:
- status
- provider
- model
- job_type
- created_at

9. Tests

Add tests for:

- User can explain a document with extracted text.
- User cannot explain a document without extracted text.
- User cannot explain another user’s document.
- User cannot explain document with insufficient credits.
- Explanation creates AIJob.
- Explanation creates AIResponse.
- Explanation creates DocumentAnalysis.
- Successful explanation deducts exactly 1 credit.
- Failed LLM call does not deduct credits.
- Invalid JSON response retries once.
- Invalid JSON after retry marks job failed.
- Failed job does not charge wallet.
- Mock provider returns valid structured response.
- API explain endpoint returns queued/running status.
- Analysis endpoint returns completed analysis.
- Job status endpoint returns expected status.
- Admin models are registered.

10. Constraints

Do not implement:
- WhatsApp sending.
- WhatsApp webhook.
- Digital Virgo payments.
- OCR or vision document understanding.
- Speech-to-text.
- Pasted text explanation.
- Message generation.
- Generic chatbot.
- Inwi support mode.
- Native app.

This milestone is only about:
- Taking already extracted document text.
- Generating Darija explanation.
- Saving structured AI result.
- Showing result in PWA.
- Charging credits safely only on success.

11. After implementation

Show:
- Files changed
- New models
- New services
- New API endpoints
- New templates
- New tests
- How to run migrations
- How to run tests

## Milestone 4 — Extended (Authentication PWA and WhatsApp)
Implement the authentication bridge for PWA and WhatsApp.

Goal:
PWA views should use normal Django login/session authentication. WhatsApp webhooks should not require login but should map inbound WhatsApp identities to User accounts.

Requirements:

1. PWA auth
- Configure LOGIN_URL, LOGIN_REDIRECT_URL, and LOGOUT_REDIRECT_URL.
- Add LoginRequiredMixin to protected PWA views.
- Add a require_auth(request) helper for Django Ninja APIs.

2. Identity models
Create or complete:
- PhoneIdentity
- WhatsAppIdentity

PhoneIdentity fields:
- user
- phone_number
- is_verified
- verified_at
- created_at

WhatsAppIdentity fields:
- user nullable at first if needed
- wa_id
- phone_number nullable
- display_name nullable
- is_linked
- linked_at
- last_seen_at
- raw_profile JSON
- created_at
- updated_at

3. WhatsApp identity service
Create:
apps/accounts/services/whatsapp_identity.py

Implement:
- find_or_create_whatsapp_identity(wa_id, phone_number=None, display_name=None, raw_profile=None)
- link_whatsapp_identity_to_user(identity, user)
- get_user_from_whatsapp_identity(wa_id)

4. Magic link service
Create:
apps/accounts/services/magic_links.py

Implement:
- create_whatsapp_login_token(wa_identity, action=None, next_url=None)
- validate_whatsapp_login_token(token)
- consume_whatsapp_login_token(token)

Token rules:
- Signed token
- Expires after 10 minutes
- One-time use if persisted
- Redirects only to safe internal URLs
- Does not expose secrets

5. WhatsApp-to-PWA login view
Create a view:
GET /accounts/whatsapp-login/<token>/

Behavior:
- Validate token
- Find or create user
- Link WhatsApp identity to user
- Log user in using Django session
- Redirect to next_url or dashboard

6. Security
- Do not use login_required on WhatsApp webhook.
- Webhook must use provider verification/signature checks instead.
- Do not allow open redirects.
- Do not expose whether a phone number already has an account.
- Store raw WhatsApp identity data for debugging.

7. Tests
Add tests for:
- Protected PWA view redirects anonymous user to login.
- Authenticated user can access protected PWA view.
- WhatsApp webhook endpoint does not require login.
- WhatsApp identity is created from inbound message data.
- WhatsApp identity can be linked to user.
- Magic login token expires.
- Magic login token cannot be reused if one-time storage is implemented.
- Unsafe next_url is rejected.

## Milestone 5 — Pasted Text Explanation

Read AGENTS.md and the product documentation, especially:

- product/PRD.md
- product/API_SPEC.md
- product/PROMPTS.md
- product/MILESTONES.md
- product/SECURITY_PRIVACY.md

Implement Milestone 5 only: Pasted Text Explanation.

Goal:
Allow authenticated users to paste French, Arabic, formal Arabic, or mixed text and receive a structured explanation in simple Moroccan Darija. This should reuse the AIJob, PromptTemplate, wallet, and provider abstraction created in Milestone 4.

Important:
This milestone does NOT implement WhatsApp, payments, OCR, voice transcription, or generic chatbot features.

Core user story:
As a user, I can paste a piece of text into dwi.ma, spend one credit, and receive a clear Moroccan Darija explanation with key points and next steps.

Requirements:

1. Models

Reuse existing models from assistant app:

- AIJob
- PromptTemplate
- AIResponse
- SafetyFlag

If needed, create a new model in assistant app:

TextExplanation:
- id: UUID primary key
- user: ForeignKey to User
- ai_job: ForeignKey to AIJob
- original_text
- detected_text_type nullable
- summary_darija
- important_points_json
- extracted_entities_json
- unclear_points_json
- next_steps_json
- disclaimer_darija
- full_response_text
- created_at
- updated_at

If the existing AIJob/result_json structure is enough, you may avoid creating TextExplanation, but the result must be easy to retrieve and display.

2. Prompt template

Create a default active prompt template for pasted text explanation.

System prompt:

You are dwi.ma, a helpful Moroccan Darija assistant.
Your role is to explain pasted text in simple Moroccan Darija for ordinary Moroccan users.
You must only use information found in the provided text.
Do not invent facts.
If something is unclear, say: "هاد النقطة ما واضحةش فهاد النص."
If the text appears legal, medical, financial, insurance-related, banking-related, administrative, or tax-related, include a short disclaimer that this is only an explanation, not professional advice.
Use simple Moroccan Darija, not formal Arabic.
Keep the answer practical, organized, and easy to read.
Return valid JSON only.

User prompt template:

Explain this text in simple Moroccan Darija.

Text content:
{{input_text}}

Return valid JSON using this exact schema:

{
  "text_type": "string",
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

Rules:
- Return JSON only.
- Do not wrap the JSON in markdown.
- Do not add information that is not in the text.
- If a field has no information, return an empty array or empty string.
- If something is unclear, use: "هاد النقطة ما واضحةش فهاد النص."

3. Service layer

Create or update:

apps/assistant/services/text_explanation.py

Implement:

explain_text(user, input_text, output_language="darija_arabic")

Behavior:
1. Validate authenticated user.
2. Validate input text is not empty.
3. Validate input text length.
4. Check wallet balance.
5. Reserve 1 credit.
6. Create AIJob with job_type=text_explanation.
7. Load active text explanation prompt.
8. Call LLM provider.
9. Parse JSON.
10. Retry once if JSON is invalid.
11. Save AIResponse.
12. Save TextExplanation if model is created, or save structured result in AIJob.result_json.
13. Mark AIJob completed.
14. Charge reserved usage only after valid result is saved.
15. Return structured explanation.

Failure behavior:
- If text is empty, return validation error.
- If text is too long, return friendly error.
- If user has insufficient credits, do not create paid job.
- If LLM fails, mark AIJob failed.
- If LLM fails, fail the reserved usage and do not deduct credits.
- If JSON parsing fails after retry, mark AIJob failed and do not deduct credits.
- Do not expose raw technical errors to the user.

Recommended validation:
- Minimum text length: 10 characters.
- Maximum text length: configurable setting:
  TEXT_EXPLANATION_MAX_CHARS=12000

4. API endpoints using Django Ninja

Add endpoints:

POST /api/assistant/explain-text

Input:

{
  "text": "string",
  "output_language": "darija_arabic"
}

Response:

{
  "job_id": "uuid",
  "status": "queued"
}

Rules:
- Requires authenticated user.
- Requires enough credits.
- Starts Celery task if existing async job pattern is available.
- Otherwise use the same sync/async pattern used in Milestone 4.

GET /api/assistant/text-explanations/{job_id}

Response:

{
  "job_id": "uuid",
  "status": "completed",
  "text_type": "...",
  "summary_darija": "...",
  "important_points": [],
  "extracted_entities": {},
  "unclear_points": [],
  "next_steps": [],
  "disclaimer": "...",
  "full_answer": "..."
}

If there is already a generic GET /api/assistant/jobs/{job_id}, update it to support text_explanation results.

5. Celery task

Create or update:

apps/assistant/tasks.py

Task:

explain_text_task(user_id, input_text, options=None)

Behavior:
- Create or continue AIJob according to the existing pattern.
- Set status to running.
- Run text explanation service.
- Save results.
- Charge credits only on success.
- Fail usage on error.
- Store safe error message.
- Never deduct credits on failed explanation.

6. PWA templates

Create or update mobile-first Bootstrap templates:

- assistant/explain_text_form.html
- assistant/text_processing.html
- assistant/text_result.html

User flow:
1. User opens “شرح ليا نص”.
2. User sees text area.
3. User pastes text.
4. Page shows clear note: this will use 1 credit.
5. User submits.
6. Processing page polls job status with HTMX if async.
7. Result page displays structured explanation.

Result page should show:
- Text type
- Short summary
- Important points
- Names/dates/amounts/deadlines/obligations
- Unclear points
- What to do next
- Disclaimer
- Full answer
- Buttons:
  - Copy result
  - Explain another text
  - Back to dashboard

Use simple Darija UI labels where appropriate.

Suggested labels:
- “شرح ليا نص”
- “لسق النص هنا”
- “هاد العملية غادي تستعمل 1 كريدي”
- “شرح النص”
- “نسخ النتيجة”
- “شرح نص آخر”

7. Navigation/dashboard

Update dashboard to include a visible card/button:

“شرح ليا نص”

Description:
“لسق نص بالفرنسية ولا العربية، و dwi.ma يشرحو ليك بدارجة بسيطة.”

8. Admin

If TextExplanation model is created, register it in admin.

Admin should show:
- user
- ai_job
- detected_text_type
- created_at
- updated_at

Also ensure AIJob admin can filter by:
- job_type=text_explanation
- status
- provider
- model
- created_at

9. Tests

Add tests for:

- Authenticated user can submit pasted text.
- Anonymous user cannot access pasted text explanation view.
- Empty text is rejected.
- Very short text is rejected.
- Text above max length is rejected.
- User with insufficient credits cannot start explanation.
- Successful text explanation creates AIJob.
- Successful text explanation creates AIResponse.
- Successful text explanation saves structured result.
- Successful text explanation deducts exactly 1 credit.
- Failed LLM call does not deduct credits.
- Invalid JSON response retries once.
- Invalid JSON after retry marks job failed.
- Failed job does not charge wallet.
- API explain-text endpoint returns queued/running status.
- Text result endpoint returns completed explanation.
- Dashboard includes “شرح ليا نص” entry.
- Admin model is registered if TextExplanation model exists.

10. Constraints

Do not implement:
- WhatsApp sending.
- WhatsApp webhook.
- Digital Virgo payments.
- OCR or vision document understanding.
- Speech-to-text.
- Message generation.
- Generic chatbot.
- Inwi support mode.
- Native app.

This milestone is only about:
- Pasted text input.
- AI explanation in Darija.
- Structured result display.
- Safe wallet charging.
- PWA pages for text explanation.

11. After implementation

Show:
- Files changed
- New models if any
- New services
- New API endpoints
- New templates
- New tests
- How to run migrations
- How to run tests

## Milestone 6 — WhatsApp Companion
Read AGENTS.md and the product documentation, especially:

- product/PRD.md
- product/API_SPEC.md
- product/WHATSAPP_FLOWS.md
- product/MILESTONES.md
- product/SECURITY_PRIVACY.md
- product/DATA_MODEL.md

Implement Milestone 6 only: WhatsApp Companion Integration.

Goal:
Implement WhatsApp as a companion channel for dwi.ma. Users should be able to interact with dwi.ma through WhatsApp menus, send simple text messages, link their WhatsApp identity to a user account, and receive AI results generated from previous milestones.

Important:
Do not build a generic chatbot. WhatsApp must remain task-specific:
- Explain document
- Explain pasted text
- Generate message later
- Check credits
- Send result to WhatsApp
- Link to PWA for upload/payment/history

This milestone should work with a MockWhatsAppProvider first, so tests do not require real Meta credentials.

Requirements:

1. Models

Create or complete the following models in the whatsapp app.

WhatsAppWebhookEvent:
- id: UUID primary key
- event_id nullable
- payload_json
- processed boolean default false
- processing_error nullable
- received_at
- processed_at nullable

WhatsAppInboundMessage:
- id: UUID primary key
- user nullable
- wa_id
- phone_number nullable
- message_id unique
- message_type: text, audio, image, document, interactive, button, list_reply, unknown
- text_body nullable
- media_id nullable
- interactive_payload JSON nullable
- raw_payload JSON
- created_at

WhatsAppOutboundMessage:
- id: UUID primary key
- user nullable
- wa_id
- phone_number nullable
- message_id nullable
- message_type: text, interactive_buttons, interactive_list, template, document, unknown
- text_body nullable
- payload_json
- status: queued, sent, delivered, read, failed
- error_message nullable
- created_at
- updated_at

WhatsAppConversationState:
- id: UUID primary key
- user nullable
- wa_id unique
- current_state: main_menu, waiting_for_text, waiting_for_document, waiting_for_action, linked, unknown
- context JSON field
- last_seen_at
- created_at
- updated_at

2. Identity mapping

Use or create identity models in accounts app:

WhatsAppIdentity:
- user nullable
- wa_id unique
- phone_number nullable
- display_name nullable
- is_linked boolean default false
- linked_at nullable
- last_seen_at nullable
- raw_profile JSON
- created_at
- updated_at

Create service:

apps/accounts/services/whatsapp_identity.py

Implement:

- find_or_create_whatsapp_identity(wa_id, phone_number=None, display_name=None, raw_profile=None)
- link_whatsapp_identity_to_user(identity, user)
- get_user_from_whatsapp_identity(wa_id)

Rules:
- WhatsApp webhook endpoints must not require Django login.
- WhatsApp identity is based on wa_id and/or phone number from webhook payload.
- If identity is linked to a user, process using that user.
- If identity is not linked, create identity and send secure PWA link or onboarding message.

3. WhatsApp provider abstraction

Create:

apps/whatsapp/services/providers.py

Implement:

BaseWhatsAppProvider:
- send_text(to, body)
- send_interactive_buttons(to, body, buttons)
- send_interactive_list(to, body, sections)
- mark_as_read(message_id) optional

MockWhatsAppProvider:
- Stores outbound payloads locally or returns fake message IDs.
- Must be used in tests.
- Must not require Meta credentials.

MetaCloudWhatsAppProvider:
- Reads credentials from settings/environment:
  WHATSAPP_ACCESS_TOKEN
  WHATSAPP_PHONE_NUMBER_ID
  WHATSAPP_BUSINESS_ACCOUNT_ID
  WHATSAPP_VERIFY_TOKEN
  WHATSAPP_APP_SECRET
- Sends text messages through Meta Cloud API.
- Sends interactive buttons.
- Sends interactive list messages.
- Fails gracefully if credentials are missing.
- Logs provider errors safely.

Provider selection:
- WHATSAPP_PROVIDER=mock or meta
- Default to mock in local/test environments.

4. Webhook verification

Implement endpoints using Django Ninja or Django views, following existing project style:

GET /api/whatsapp/webhook

Behavior:
- Accept hub.mode
- Accept hub.challenge
- Accept hub.verify_token
- Compare verify token with WHATSAPP_VERIFY_TOKEN
- Return challenge if valid
- Return 403 if invalid

POST /api/whatsapp/webhook

Behavior:
- Do not require login.
- Verify request signature if WHATSAPP_APP_SECRET is configured.
- Store raw payload as WhatsAppWebhookEvent.
- Return 200 quickly.
- Start async processing task through Celery.
- If Celery is not available in local mode, allow sync fallback only if existing project pattern supports it.

5. Webhook processing task

Create or update:

apps/whatsapp/tasks.py

Task:

process_whatsapp_webhook_event(event_id)

Behavior:
1. Load webhook event.
2. Parse messages and statuses.
3. For inbound messages:
   - Extract wa_id
   - Extract phone number if available
   - Extract profile name if available
   - Create or update WhatsAppIdentity
   - Create WhatsAppInboundMessage
   - Update WhatsAppConversationState
   - Route message to basic workflow handler
4. For status events:
   - Update WhatsAppOutboundMessage status if message ID matches
5. Mark webhook event as processed.
6. Store safe error if processing fails.

6. Message parsing service

Create:

apps/whatsapp/services/parser.py

Implement:

- parse_webhook_payload(payload)
- extract_inbound_messages(payload)
- extract_status_updates(payload)
- normalize_message_type(raw_message)
- get_text_from_message(raw_message)
- get_interactive_reply(raw_message)

Support at least:
- text
- interactive button reply
- interactive list reply
- document metadata
- image metadata
- audio metadata
- unknown fallback

7. Workflow router

Create:

apps/whatsapp/services/router.py

Implement:

route_inbound_message(inbound_message)

Behavior:
- If user sends "menu", "salam", "السلام", "hi", or unknown first message, send main menu.
- If user selects “شرح نص”, set state to waiting_for_text.
- If user selects “شرح وثيقة”, send PWA upload link for now.
- If user selects “الرصيد ديالي”, return credit balance if user is linked; otherwise send account-link message.
- If state is waiting_for_text and user sends text, use existing text explanation service from Milestone 5 if available.
- If user is not linked and tries paid/protected action, send secure link to PWA login/linking flow.

Important:
- Do not implement open-ended AI chat.
- Unknown messages should return the menu, not call the LLM directly.

8. WhatsApp menu messages

Implement service:

apps/whatsapp/services/messages.py

Functions:

- send_main_menu(wa_id)
- send_account_link_message(wa_id)
- send_document_upload_link(wa_id, signed_url)
- send_text_explanation_prompt(wa_id)
- send_credit_balance(wa_id, balance)
- send_processing_message(wa_id)
- send_error_message(wa_id, safe_message)
- send_result_message(wa_id, result_text)

Main menu copy:

Salam 👋 Ana dwi.ma.
شنو بغيتي ندير ليك؟

1. نشرح ليك وثيقة
2. نشرح ليك نص
3. نكتب ليك رسالة
4. نشوف الرصيد ديالك

Use interactive buttons or list messages where supported.
If interactive messages are not available in mock/local mode, send plain text fallback.

9. Send result to WhatsApp

Add endpoint:

POST /api/whatsapp/send-result

Input:
{
  "job_id": "uuid",
  "phone_number": "+2126XXXXXXXX"
}

Behavior:
- Requires authenticated PWA user.
- Verify job belongs to user.
- Verify job is completed.
- Find linked WhatsAppIdentity for user or use provided phone number if allowed by current implementation.
- Send result_text or full_answer_darija to WhatsApp.
- Create WhatsAppOutboundMessage.
- Return send status.

Also add UI button on result pages:
- “Send to WhatsApp”
- “صيفط النتيجة للواتساب”

10. PWA account linking

If not already implemented, add minimal WhatsApp linking support:

- User can enter WhatsApp phone number in settings.
- System stores it as unverified or linked depending on existing auth flow.
- Full OTP verification can be deferred if not implemented yet.
- Add clear TODO comments where production verification is required.

If magic link service already exists:
- Use it to link WhatsApp identity to authenticated user.
- Links must expire.
- Do not allow unsafe external redirects.

11. API endpoints

Add:

GET /api/whatsapp/webhook
POST /api/whatsapp/webhook
POST /api/whatsapp/send-result
GET /api/whatsapp/conversation-state
POST /api/whatsapp/send-test-message

Rules:
- send-test-message should be staff-only or debug-only.
- webhook endpoints must not require login.
- protected endpoints must require authenticated user.

12. Admin

Register:

- WhatsAppWebhookEvent
- WhatsAppInboundMessage
- WhatsAppOutboundMessage
- WhatsAppConversationState
- WhatsAppIdentity if model lives in accounts

Admin should show:
- wa_id
- user
- message_type
- status
- current_state
- processed
- created_at
- updated_at

Add filters:
- message_type
- status
- processed
- current_state
- created_at

13. Settings

Add to settings and .env.example:

WHATSAPP_PROVIDER=mock
WHATSAPP_VERIFY_TOKEN=
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_BUSINESS_ACCOUNT_ID=
WHATSAPP_APP_SECRET=
WHATSAPP_API_VERSION=v23.0
WHATSAPP_DEFAULT_COUNTRY_CODE=212

14. Tests

Add tests for:

Webhook verification:
- Valid verify token returns challenge.
- Invalid verify token returns 403.

Webhook POST:
- Webhook POST does not require login.
- Raw webhook event is stored.
- Webhook returns 200 quickly.
- Processing task is dispatched or sync fallback runs.

Parsing:
- Text message is parsed correctly.
- Interactive button reply is parsed correctly.
- Interactive list reply is parsed correctly.
- Unknown message type does not crash parser.

Identity:
- WhatsAppIdentity is created from inbound wa_id.
- Existing WhatsAppIdentity is reused.
- Linked identity maps to user.
- Unlinked identity receives account-link message for protected actions.

Conversation routing:
- “salam” sends main menu.
- “menu” sends main menu.
- Selecting “شرح نص” sets state to waiting_for_text.
- Waiting-for-text state processes user text using existing text explanation flow if available.
- Selecting “شرح وثيقة” sends PWA upload link.
- Selecting “الرصيد ديالي” returns wallet balance for linked user.
- Unlinked user asking for credits receives link-account message.

Outbound provider:
- Mock provider returns fake message ID.
- Outbound message is stored.
- Provider failure marks outbound message as failed.

Send result:
- Authenticated user can send completed AI result to WhatsApp.
- User cannot send another user’s result.
- Incomplete job cannot be sent.
- Missing WhatsApp identity returns friendly error.
- Successful send creates WhatsAppOutboundMessage.

Security:
- Webhook signature check is used if WHATSAPP_APP_SECRET is configured.
- Unsafe redirect URLs are rejected if account-link flow is used.

15. Constraints

Do not implement:
- Digital Virgo payments.
- Real payment prompts beyond existing wallet balance.
- Voice transcription.
- WhatsApp media document upload processing.
- OCR.
- Generic chatbot.
- Inwi support mode.
- Native mobile app.
- Marketing templates.

This milestone is only about:
- WhatsApp webhook.
- WhatsApp identity mapping.
- Mock and Meta provider abstraction.
- Basic task-specific menu.
- Result delivery to WhatsApp.
- Integration with existing text explanation and wallet where available.

16. After implementation

Show:
- Files changed
- New models
- New services
- New API endpoints
- New templates/buttons
- New tests
- New environment variables
- How to run migrations
- How to run WhatsApp tests
- How to test locally with mock provider
- What is needed to switch to real Meta Cloud API credentials


## Milestone 7 — Voice Transcription and Message Generation

Read AGENTS.md and the product documentation, especially:

- product/PRD.md
- product/API_SPEC.md
- product/PROMPTS.md
- product/MILESTONES.md
- product/DATA_MODEL.md
- product/SECURITY_PRIVACY.md
- product/WHATSAPP_FLOWS.md

Implement Milestone 7 only: Voice-to-Message Generation.

Goal:
Allow authenticated users to upload or record a Darija voice note, transcribe it, and generate a useful professional message in French, Arabic, or polished Darija. This milestone should reuse the existing AIJob, wallet, provider abstraction, and PWA result infrastructure from previous milestones.

Important:
This is not a generic voice chatbot. The voice note is used only as input for a controlled workflow:
- User explains what they want in Darija.
- System transcribes the voice note.
- System generates a professional message.

Do not implement open-ended voice conversation.

Core user story:
As a user, I can send or upload a Darija voice note saying what I want to communicate, choose the target format, spend credits, and receive a polished message that I can copy or send to WhatsApp.

Examples:
- Darija voice note → professional French email
- Darija voice note → professional Arabic letter/message
- Darija voice note → polished Darija WhatsApp message
- Darija voice note → short polite reply

Requirements:

1. Models

Create or complete the following models in the audio app.

VoiceNote:
- id: UUID primary key
- user: ForeignKey to User
- audio_file
- original_filename nullable
- file_type nullable
- file_size nullable
- sha256_hash nullable
- source: choices = pwa, whatsapp, admin
- whatsapp_media_id nullable
- duration_seconds nullable
- status: choices = uploaded, transcribing, transcribed, transcription_failed, processing, completed, failed, deleted
- transcription_error nullable
- deleted_at nullable
- created_at
- updated_at

TranscriptionJob:
- id: UUID primary key
- voice_note: ForeignKey or OneToOneField to VoiceNote
- provider
- model
- status: choices = queued, running, completed, failed
- transcript
- language_detected nullable
- confidence nullable
- raw_response_json nullable
- error_message nullable
- latency_ms nullable
- created_at
- updated_at
- completed_at nullable

Create or complete the following model in assistant app if not already present.

MessageGeneration:
- id: UUID primary key
- user: ForeignKey to User
- ai_job: ForeignKey to AIJob
- voice_note nullable
- transcription_job nullable
- input_text
- target_format choices:
  - professional_french_email
  - professional_arabic_message
  - polished_darija_whatsapp
  - short_reply
- tone choices:
  - neutral
  - polite
  - polite_firm
  - friendly
  - formal
- generated_message
- created_at
- updated_at

If the project already stores generated outputs only in AIJob.result_json, that is acceptable, but the result must be easy to retrieve and display.

2. Audio validation

Accept only:
- mp3
- mp4
- m4a
- wav
- webm
- ogg
- opus

Add settings:

AUDIO_MAX_UPLOAD_MB=15
ALLOWED_AUDIO_EXTENSIONS=mp3,mp4,m4a,wav,webm,ogg,opus
TRANSCRIPTION_PROVIDER=mock
TRANSCRIPTION_MODEL=mock-transcribe
OPENAI_API_KEY=

Validation rules:
- Reject files larger than AUDIO_MAX_UPLOAD_MB.
- Reject unsupported file extensions.
- Reject empty files.
- Save original filename.
- Calculate SHA256 hash.
- Store file size.
- Do not expose uploaded audio files publicly.
- Store audio files securely.
- Do not delete audio automatically in this milestone unless deletion logic already exists.

3. Transcription provider abstraction

Create:

apps/audio/services/providers.py

Implement:

BaseTranscriptionProvider:
- transcribe(audio_file_path_or_file, language_hint=None)

MockTranscriptionProvider:
- Returns a predictable Darija transcript for tests.
- Must not require real API keys.

OpenAITranscriptionProvider:
- Reads OPENAI_API_KEY from settings/environment.
- Reads TRANSCRIPTION_MODEL from settings/environment.
- Uses the configured OpenAI transcription model.
- Fails gracefully if API key is missing.
- Stores safe error messages.
- Does not crash Celery workers.

Provider selection:
- TRANSCRIPTION_PROVIDER=mock or openai
- Default to mock in local/test environments.

4. Audio service layer

Create:

apps/audio/services/audio.py

Implement:

- calculate_audio_hash(file)
- validate_audio_file(file)
- create_voice_note(user, file, source="pwa")
- delete_voice_note(voice_note, user)

Create:

apps/audio/services/transcription.py

Implement:

- transcribe_voice_note(voice_note_id, user=None)

Behavior:
1. Load voice note.
2. Verify ownership if user is provided.
3. Set VoiceNote status to transcribing.
4. Create TranscriptionJob with status running.
5. Call transcription provider.
6. Save transcript.
7. Mark TranscriptionJob completed.
8. Mark VoiceNote transcribed.
9. On failure, mark both failed and save safe error.

Important:
- Transcription itself should not charge wallet credits unless you decide this task consumes credit separately.
- For MVP, charge only when final message generation succeeds.

5. Message generation prompt

Create a default active prompt template for message generation.

System prompt:

You are dwi.ma, a Moroccan Darija assistant that helps users turn informal Darija instructions into useful professional messages.
You must preserve the user's intent.
Do not add facts that the user did not provide.
If key information is missing, add clear placeholders like [اسم الشركة], [التاريخ], [الاسم], or [المبلغ].
Do not invent names, dates, amounts, or commitments.
Return valid JSON only.

User prompt template:

User instruction in Darija:
{{input_text}}

Target format:
{{target_format}}

Tone:
{{tone}}

Generate a message based only on the user instruction.

Return valid JSON using this exact schema:

{
  "detected_intent": "string",
  "missing_information": ["string"],
  "generated_message": "string",
  "suggested_subject": "string",
  "notes_darija": "string"
}

Rules:
- Return JSON only.
- Do not wrap JSON in markdown.
- Preserve the user's intent.
- Do not add facts not provided by the user.
- If important information is missing, use placeholders.
- The generated message should match the requested target format.
- If target format is professional_french_email, write the message in French.
- If target format is professional_arabic_message, write the message in Arabic.
- If target format is polished_darija_whatsapp, write the message in Moroccan Darija.
- If target format is short_reply, write a short useful reply.

6. Message generation service

Create:

apps/assistant/services/message_generation.py

Implement:

generate_message_from_text(
    user,
    input_text,
    target_format,
    tone="polite",
    voice_note=None,
    transcription_job=None
)

Behavior:
1. Validate authenticated user.
2. Validate input text is not empty.
3. Validate target_format is allowed.
4. Validate tone is allowed.
5. Check wallet balance.
6. Reserve 1 credit.
7. Create AIJob with job_type=message_generation.
8. Load active message generation prompt.
9. Call LLM provider.
10. Parse JSON.
11. Retry once if JSON invalid.
12. Save AIResponse.
13. Save MessageGeneration or AIJob.result_json.
14. Mark AIJob completed.
15. Charge reserved usage only after valid generated message is saved.
16. Return structured result.

Failure behavior:
- If text is empty, return validation error.
- If user has insufficient credits, do not create paid job.
- If LLM fails, mark AIJob failed.
- If LLM fails, fail reserved usage and do not deduct credits.
- If JSON parsing fails after retry, mark AIJob failed and do not deduct credits.
- Do not expose raw technical errors to user.

7. Voice-to-message service

Create:

apps/audio/services/voice_to_message.py

Implement:

generate_message_from_voice_note(
    user,
    voice_note_id,
    target_format,
    tone="polite"
)

Behavior:
1. Verify voice note belongs to user.
2. If voice note is not transcribed, transcribe it.
3. Use transcript as input_text.
4. Call generate_message_from_text.
5. Save linkage to VoiceNote and TranscriptionJob.
6. Mark VoiceNote completed if message generation succeeds.
7. If generation fails, do not deduct credits.

8. Celery tasks

Create or update:

apps/audio/tasks.py

Tasks:

transcribe_voice_note_task(voice_note_id)

Behavior:
- Run transcription.
- Mark status.
- Store safe errors.

generate_message_from_voice_note_task(user_id, voice_note_id, target_format, tone)

Behavior:
- Ensure transcription exists.
- Run message generation.
- Charge credits only on successful message generation.
- Store result.
- Never deduct credits on failed transcription or failed message generation.

If existing async pattern from Milestones 4 and 5 uses AIJob first, follow that pattern consistently.

9. API endpoints using Django Ninja

Add endpoints:

POST /api/audio/upload

Multipart upload.

Input:
- audio file
- source=pwa

Response:
{
  "voice_note_id": "uuid",
  "status": "uploaded",
  "filename": "...",
  "file_size": 12345
}

POST /api/audio/{voice_note_id}/transcribe

Response:
{
  "transcription_job_id": "uuid",
  "status": "queued|running|completed"
}

GET /api/audio/{voice_note_id}/transcript

Response:
{
  "voice_note_id": "uuid",
  "status": "transcribed",
  "transcript": "..."
}

POST /api/assistant/generate-message

Input:
{
  "input_text": "string",
  "target_format": "professional_french_email",
  "tone": "polite"
}

Response:
{
  "job_id": "uuid",
  "status": "queued|running|completed"
}

POST /api/audio/{voice_note_id}/generate-message

Input:
{
  "target_format": "professional_french_email",
  "tone": "polite"
}

Response:
{
  "job_id": "uuid",
  "voice_note_id": "uuid",
  "status": "queued|running|completed"
}

GET /api/assistant/message-generations/{job_id}

Response:
{
  "job_id": "uuid",
  "status": "completed",
  "detected_intent": "...",
  "missing_information": [],
  "generated_message": "...",
  "suggested_subject": "...",
  "notes_darija": "..."
}

DELETE /api/audio/{voice_note_id}

Behavior:
- Mark voice note deleted.
- Delete physical file if project deletion service supports that.
- User can only delete own voice note.

10. PWA templates

Create mobile-first Bootstrap templates:

- audio/upload.html
- audio/transcription_result.html
- assistant/generate_message_form.html
- assistant/message_processing.html
- assistant/message_result.html

User flow A: voice note to message
1. User opens “كتب ليا رسالة”.
2. User chooses “سجل/طلع فويس”.
3. User uploads audio file.
4. User selects:
   - Professional French email
   - Professional Arabic message
   - Polished Darija WhatsApp message
   - Short reply
5. User selects tone.
6. Page shows: “هاد العملية غادي تستعمل 1 كريدي من بعد ما تخرج النتيجة بنجاح.”
7. User submits.
8. System transcribes voice note.
9. System generates message.
10. Result page shows transcript and generated message.

User flow B: text to message
1. User opens “كتب ليا رسالة”.
2. User types Darija instruction.
3. User chooses target format and tone.
4. System generates message.

Result page should show:
- Original transcript/input
- Detected intent
- Missing information
- Suggested subject if available
- Generated message
- Notes in Darija
- Buttons:
  - Copy message
  - Generate another message
  - Send result to WhatsApp if Milestone 6 supports it
  - Back to dashboard

Suggested UI labels:
- “كتب ليا رسالة”
- “طلع فويس نوت”
- “شنو النوع ديال الرسالة؟”
- “إيميل مهني بالفرنسية”
- “رسالة مهنية بالعربية”
- “رسالة واتساب بدارجة مزيانة”
- “جواب قصير”
- “نسخ الرسالة”
- “صيفط للواتساب”

11. Dashboard/navigation

Update dashboard to include:

Card:
Title: “كتب ليا رسالة”
Description:
“قول شنو بغيتي بدارجة، و dwi.ma يكتبها ليك بطريقة مهنية.”

12. WhatsApp integration, limited

If Milestone 6 is implemented:
- Add route for menu item “نكتب ليك رسالة”.
- For now, if user selects it from WhatsApp, send PWA link to the message generation page.
- Do not process WhatsApp audio media directly unless existing media download service is already implemented.
- Add TODO for WhatsApp audio media processing in a future milestone.

13. Admin

Register:

- VoiceNote
- TranscriptionJob
- MessageGeneration if created

Admin should show:
- user
- status
- provider
- model
- source
- target_format
- tone
- created_at
- completed_at

Add filters:
- status
- provider
- model
- source
- target_format
- created_at

14. Tests

Add tests for:

Audio validation:
- Valid audio upload succeeds.
- Unsupported audio extension is rejected.
- Empty audio file is rejected.
- Oversized audio file is rejected.
- SHA256 hash is calculated.
- VoiceNote is created with correct metadata.

Transcription:
- Mock transcription provider returns expected transcript.
- TranscriptionJob is created.
- Successful transcription marks VoiceNote as transcribed.
- Failed transcription marks VoiceNote as transcription_failed.
- Transcription failure does not deduct credits.

Message generation:
- User can generate message from text.
- User can generate message from transcribed voice note.
- Empty text is rejected.
- Invalid target_format is rejected.
- Invalid tone is rejected.
- User with insufficient credits cannot generate message.
- Successful message generation creates AIJob.
- Successful message generation creates AIResponse.
- Successful message generation saves structured result.
- Successful message generation deducts exactly 1 credit.
- Failed LLM call does not deduct credits.
- Invalid JSON response retries once.
- Invalid JSON after retry marks job failed.
- Failed message generation does not charge wallet.

Security:
- User cannot access another user’s voice note.
- User cannot delete another user’s voice note.
- Anonymous user cannot access voice upload/generation pages.

API:
- Audio upload endpoint returns voice_note_id.
- Transcribe endpoint returns job status.
- Transcript endpoint returns transcript.
- Generate-message endpoint returns job_id.
- Message-generation result endpoint returns generated message.

PWA:
- Dashboard includes “كتب ليا رسالة”.
- Message result page displays generated message.
- Copy button exists.

WhatsApp limited integration:
- Selecting “نكتب ليك رسالة” from WhatsApp sends PWA link if router exists.

15. Constraints

Do not implement:
- Digital Virgo payments.
- Full WhatsApp audio media download and processing unless already available.
- OCR.
- Generic chatbot.
- Inwi support mode.
- Native mobile app.
- Voice response / text-to-speech.
- Human review workflow.
- Advanced prompt library.

This milestone is only about:
- Audio upload.
- Transcription provider abstraction.
- Voice note transcription.
- Message generation from transcript or text.
- Safe wallet charging.
- PWA pages for message generation.
- Limited WhatsApp routing to PWA.

16. After implementation

Show:
- Files changed
- New models
- New services
- New API endpoints
- New templates
- New tests
- New environment variables
- How to run migrations
- How to run audio/message tests
- How to test locally with mock transcription provider
- How to switch to OpenAI transcription provider