# dwi.ma Product Requirements Document

## 1. Product Overview

**Product name:** dwi.ma  
**Market:** Morocco  
**Product type:** Mobile-first SaaS / PWA with WhatsApp companion  
**Primary language:** Moroccan Darija  
**Backend:** Django + Django Ninja  
**Payments:** Digital Virgo  
**AI providers for MVP:** OpenAI and/or Anthropic

dwi.ma helps Moroccan users understand documents and generate useful messages in simple Moroccan Darija.

The MVP should focus on concrete tasks, not a generic chatbot.

---

## 2. Product Vision

Many Moroccans receive documents in French, formal Arabic, legal/administrative language, or technical wording they do not fully understand.

dwi.ma gives them a simple way to:

1. Upload a document.
2. Receive a clear Moroccan Darija explanation.
3. Extract important dates, amounts, obligations, names, and deadlines.
4. Understand what they may need to do next.
5. Rewrite informal Darija instructions into professional messages.

The long-term opportunity is to become a trusted Darija AI layer for citizens, students, small businesses, and potentially telecom partners.

---

## 3. Strategic Positioning

### dwi.ma is

- A document explainer.
- A Darija-first AI utility.
- A practical writing assistant.
- A WhatsApp-friendly service.
- A future telecom/SME digital inclusion product.

### dwi.ma is not in MVP

- Not a legal advisor.
- Not a medical advisor.
- Not an accountant.
- Not a generic chatbot.
- Not a native mobile app.
- Not a self-hosted LLM platform.
- Not a telecom white-label product yet.

---

## 4. Target Users

### Persona 1: Ordinary Moroccan citizen

**Need:** Understand administrative, telecom, banking, school, or formal documents.  
**Pain:** The document is in French/formal Arabic or uses difficult wording.  
**Value:** Upload and get a simple explanation in Darija.

### Persona 2: Student or job seeker

**Need:** Understand academic/job documents and write formal messages.  
**Pain:** They think in Darija but need professional French or Arabic.  
**Value:** Generate emails, requests, and replies from Darija instructions.

### Persona 3: Small business owner

**Need:** Understand supplier messages, quotes, invoices, and business documents.  
**Pain:** They need professional communication without hiring an assistant.  
**Value:** Turn a Darija voice note into a polished message.

### Persona 4: Future telecom partner

**Need:** Better Darija self-service for customers.  
**Pain:** Customers need help understanding bills, offers, support steps, and contracts.  
**Value:** dwi.ma can later become a white-label Darija support layer.

---

## 5. MVP Scope

### Must-have

1. User account using phone number.
2. Free trial credits.
3. Document upload from PWA.
4. Text extraction for text-based PDFs.
5. AI explanation in Moroccan Darija.
6. Pasted text explanation.
7. Darija-to-professional-message generation.
8. WhatsApp result delivery.
9. Credit wallet.
10. Digital Virgo payment skeleton.
11. Admin visibility.
12. Privacy consent.
13. Document deletion.

### Should-have

1. WhatsApp interactive menu.
2. Audio upload and transcription.
3. User feedback after each result.
4. AI job retry on invalid JSON.
5. Basic usage analytics.

### Could-have later

1. Darija voice response.
2. Export explanation as PDF.
3. Saved templates.
4. Referral system.
5. Moroccan procedure RAG.
6. Telecom white-label dashboard.

### Out of scope

1. Native mobile app.
2. React/Next.js frontend.
3. Generic chatbot.
4. Self-hosted Atlas model.
5. Medical diagnosis.
6. Legal advice.
7. Accounting automation.

---

## 6. Core User Journeys

### Journey A: Explain a document

1. User opens dwi.ma on mobile.
2. User selects “شرح ليا وثيقة”.
3. User uploads PDF or image.
4. User accepts privacy notice.
5. System processes the document asynchronously.
6. System extracts text or uses vision/PDF AI if needed.
7. LLM generates Darija explanation.
8. User sees result page.
9. User can send result to WhatsApp.
10. Credit is consumed only after successful result.

### Journey B: Explain pasted text

1. User selects “شرح ليا نص”.
2. User pastes text.
3. System generates simple Darija explanation.
4. User can copy or send result to WhatsApp.

### Journey C: Generate professional message

1. User selects “كتب ليا رسالة”.
2. User enters Darija text or uploads voice note.
3. System transcribes if audio.
4. User chooses output:
   - Professional French email.
   - Professional Arabic message.
   - Polished Darija WhatsApp message.
5. System generates message.
6. User copies or sends it to WhatsApp.

### Journey D: WhatsApp entry point

1. User sends “Salam” to the dwi.ma WhatsApp number.
2. Bot shows menu.
3. User selects a task.
4. For simple tasks, bot continues inside WhatsApp.
5. For uploads/payment/history, bot sends PWA link.

### Journey E: Payment

1. User runs out of credits.
2. User selects credit package.
3. User starts Digital Virgo payment flow.
4. Digital Virgo sends callback.
5. Backend verifies transaction.
6. Credits are added.
7. User receives confirmation.

---

## 7. Functional Requirements

### FR1 — Accounts

- User can be identified by phone number.
- User can optionally add email and name.
- User profile stores WhatsApp opt-in status.
- User profile stores preferred output language/channel.

### FR2 — Wallet

- New users receive free credits.
- Each billable action creates a usage event.
- Credits are charged only on successful completion.
- Failed jobs do not consume credits.
- Admin can refund or add credits.

### FR3 — Document upload

- Accept PDF, JPG, JPEG, PNG, WEBP.
- Enforce file size limit.
- Store source as PWA or WhatsApp.
- Track processing status.
- Allow deletion.

### FR4 — Text extraction

- Extract text from text-based PDFs.
- Use OCR/vision/PDF AI for scanned or image documents.
- Store extracted text and extraction method.

### FR5 — Document explanation

- Generate structured answer in Darija.
- Identify document type.
- Summarize.
- Extract important points.
- Extract names, dates, amounts, deadlines, obligations.
- Explain what user may need to do next.
- Add disclaimer for sensitive categories.
- Avoid invented facts.

### FR6 — Pasted text explanation

- User can paste text and get Darija explanation.
- Same structure as document explanation.

### FR7 — Voice and message generation

- User can submit text or audio.
- Audio is transcribed.
- User chooses target format.
- System generates professional output.

### FR8 — WhatsApp integration

- Receive inbound webhook events.
- Store raw payloads.
- Process asynchronously.
- Send outbound result messages.
- Send simple menu messages.

### FR9 — Payments

- Display credit packages.
- Start payment transaction.
- Receive Digital Virgo callback.
- Verify transaction.
- Add credits idempotently.

### FR10 — Admin

- View users, jobs, documents, payments, errors.
- Retry failed jobs.
- Refund credits.
- Delete documents.
- View raw provider payloads.

---

## 8. Non-Functional Requirements

### Performance

- Webhooks return within 2 seconds.
- AI jobs run asynchronously.
- Simple PDF explanation target: under 60 seconds.
- UI should show progress while processing.

### Reliability

- External calls have retry logic.
- Webhook processing is idempotent.
- Payment callback is idempotent.
- Failed AI responses do not charge user.

### Security

- Use HTTPS in production.
- Use private media storage.
- Validate uploaded files.
- Store secrets in environment variables.
- Never expose raw files publicly.

### Privacy

- Require consent before document processing.
- Allow document deletion.
- Do not train models on user documents by default.
- Log consent and deletion actions.

---

## 9. Success Metrics

### Activation

- First document uploaded.
- First explanation completed.
- First result sent to WhatsApp.

### Quality

- User rating after result.
- Percent marked “helpful”.
- Percent marked “unclear”.
- Failed processing rate.

### Monetization

- Free-to-paid conversion.
- Payment success rate.
- Credits purchased per user.
- Repeat purchase rate.

### Operations

- Average processing cost.
- Average job latency.
- WhatsApp delivery success rate.
- Payment callback success rate.

---

## 10. Pricing Hypothesis

Initial credit packages:

| Product | Price | Credits |
|---|---:|---:|
| Free trial | 0 MAD | 3 |
| One document | 5 MAD | 1 |
| Mini pack | 19 MAD | 10 |
| Pro pack | 49 MAD | 30 |
| SME test pack | 99 MAD | 100 |

Credit consumption:

| Action | Credits |
|---|---:|
| Explain pasted text | 1 |
| Explain document | 1 |
| Generate message from text | 1 |
| Transcribe + generate from voice | 1 or 2 |
| Send result to WhatsApp | 0 initially |

---

## 11. Launch Acceptance Criteria

The MVP is ready for private testing when:

1. User can access mobile-first dashboard.
2. User receives free credits.
3. User can upload PDF/image.
4. User can get Darija explanation.
5. User can paste text and get Darija explanation.
6. User can generate a professional message from Darija input.
7. User can receive result on WhatsApp.
8. User can buy credits or use payment skeleton.
9. Credits are charged only after successful jobs.
10. User can delete uploaded documents.
11. Admin can inspect jobs, users, and payments.
12. Main flows are covered by tests.
