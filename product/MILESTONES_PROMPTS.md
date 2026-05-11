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