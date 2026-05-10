from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class FoundationTests(TestCase):
    def test_project_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_custom_user_creation_with_phone(self):
        user = get_user_model().objects.create_user(phone_number="+212600000001", password="secret")
        self.assertEqual(user.phone_number, "+212600000001")

    def test_superuser_creation_with_phone(self):
        admin = get_user_model().objects.create_superuser(phone_number="+212600000002", password="secret")
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)

    def test_dashboard_renders_for_authenticated_user(self):
        user = get_user_model().objects.create_user(phone_number="+212600000003", password="secret")
        client = Client()
        client.force_login(user)
        response = client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
