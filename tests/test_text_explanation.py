from unittest.mock import patch

from django.contrib.admin.sites import site
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings

from apps.assistant.models import AIJob, AIResponse, PromptTemplate, TextExplanation
from apps.assistant.services.text_explanation import explain_text
from apps.wallet.services import get_wallet


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, TEXT_EXPLANATION_MAX_CHARS=50)
class TextExplanationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(phone_number="+212633333333", password="secret")
        self.client = Client()
        self.client.force_login(self.user)
        PromptTemplate.objects.create(
            name="text_explanation",
            version="v1",
            active=True,
            system_prompt="sys",
            user_prompt_template="{{input_text}}",
        )

    def test_anonymous_cannot_access_view(self):
        anon = Client()
        resp = anon.get("/assistant/explain-text/")
        self.assertEqual(resp.status_code, 302)

    def test_authenticated_user_can_submit_text(self):
        with patch("apps.assistant.services.providers.MockLLMProvider.generate") as gen:
            gen.return_value = '{"text_type":"x","short_summary_darija":"s","important_points_darija":[],"extracted_entities":{"names":[],"dates":[],"amounts":[],"deadlines":[],"obligations":[]},"unclear_points_darija":[],"next_steps_darija":[],"disclaimer_darija":"","full_answer_darija":"f"}'
            r = self.client.post("/api/assistant/explain-text", data={"text": "bonjour ceci est un texte long", "output_language": "darija_arabic"}, content_type="application/json")
            self.assertEqual(r.status_code, 200)

    def test_empty_short_and_long_validation(self):
        self.assertRaises(Exception, explain_text, self.user, "")
        self.assertRaises(Exception, explain_text, self.user, "123456789")
        self.assertRaises(Exception, explain_text, self.user, "a" * 51)

    def test_insufficient_credits(self):
        wallet = get_wallet(self.user)
        wallet.balance = 0
        wallet.save()
        r = self.client.post("/api/assistant/explain-text", data={"text": "bonjour ceci est un texte long"}, content_type="application/json")
        self.assertEqual(r.status_code, 402)

    def test_success_creates_models_and_charges_one_credit(self):
        before = get_wallet(self.user).balance
        explain_text(self.user, "bonjour ceci est un texte long")
        self.assertEqual(AIJob.objects.filter(job_type=AIJob.JobType.TEXT_EXPLANATION, status=AIJob.Status.COMPLETED).count(), 1)
        self.assertEqual(AIResponse.objects.count(), 1)
        self.assertEqual(TextExplanation.objects.count(), 1)
        self.assertEqual(get_wallet(self.user).balance, before - 1)

    def test_llm_failure_does_not_deduct(self):
        before = get_wallet(self.user).balance
        with patch("apps.assistant.services.providers.MockLLMProvider.generate", side_effect=Exception("boom")):
            self.assertRaises(Exception, explain_text, self.user, "bonjour ceci est un texte long")
        self.assertEqual(get_wallet(self.user).balance, before)

    def test_invalid_json_retries_once_then_fails(self):
        before = get_wallet(self.user).balance
        with patch("apps.assistant.services.providers.MockLLMProvider.generate", side_effect=["not json", "still bad"]):
            self.assertRaises(Exception, explain_text, self.user, "bonjour ceci est un texte long")
        job = AIJob.objects.filter(job_type=AIJob.JobType.TEXT_EXPLANATION).latest("created_at")
        self.assertEqual(job.status, AIJob.Status.FAILED)
        self.assertEqual(get_wallet(self.user).balance, before)

    def test_result_endpoint_and_dashboard(self):
        out = explain_text(self.user, "bonjour ceci est un texte long")
        job = out["job"]
        r = self.client.get(f"/api/assistant/text-explanations/{job.id}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "completed")
        dash = self.client.get("/dashboard/")
        self.assertContains(dash, "شرح ليا نص")

    def test_text_explanation_admin_registered(self):
        self.assertIn(TextExplanation, site._registry)
