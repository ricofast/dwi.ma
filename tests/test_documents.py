import hashlib

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings

from apps.documents.models import UploadedDocument
from apps.documents.services.extraction import extract_text
from apps.wallet.services import get_wallet


def text_pdf_bytes():
    return b"%PDF-1.1\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 300 300]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj\n4 0 obj<</Length 44>>stream\nBT /F1 18 Tf 72 200 Td (Hello dwi) Tj ET\nendstream endobj\n5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF"


def scanned_pdf_bytes():
    return b"%PDF-1.1\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 300 300]>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF"


@override_settings(DOCUMENT_MAX_UPLOAD_MB=1, ALLOWED_DOCUMENT_EXTENSIONS=["pdf", "jpg", "jpeg", "png", "webp"])
class DocumentTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(phone_number="+212611111111", password="secret")
        self.other = get_user_model().objects.create_user(phone_number="+212622222222", password="secret")
        self.client = Client()
        self.client.force_login(self.user)

    def test_pdf_upload_succeeds(self):
        f = SimpleUploadedFile("file.pdf", text_pdf_bytes(), content_type="application/pdf")
        response = self.client.post("/api/documents/upload", {"file": f, "consent_accepted": "true", "source": "pwa"})
        self.assertEqual(response.status_code, 200)

    def test_image_upload_succeeds_and_extraction_unsupported(self):
        f = SimpleUploadedFile("pic.jpg", b"abc", content_type="image/jpeg")
        response = self.client.post("/api/documents/upload", {"file": f, "consent_accepted": "true"})
        doc_id = response.json()["document_id"]
        extract = self.client.post(f"/api/documents/{doc_id}/extract")
        self.assertEqual(extract.status_code, 200)
        self.assertEqual(extract.json()["status"], UploadedDocument.Status.EXTRACTION_FAILED)

    def test_unsupported_extension_rejected(self):
        f = SimpleUploadedFile("bad.exe", b"abc")
        response = self.client.post("/api/documents/upload", {"file": f, "consent_accepted": "true"})
        self.assertEqual(response.status_code, 400)

    def test_too_large_rejected(self):
        f = SimpleUploadedFile("big.pdf", b"a" * (2 * 1024 * 1024), content_type="application/pdf")
        response = self.client.post("/api/documents/upload", {"file": f, "consent_accepted": "true"})
        self.assertEqual(response.status_code, 400)

    def test_empty_rejected(self):
        f = SimpleUploadedFile("empty.pdf", b"", content_type="application/pdf")
        response = self.client.post("/api/documents/upload", {"file": f, "consent_accepted": "true"})
        self.assertEqual(response.status_code, 400)

    def test_sha256_and_metadata_saved(self):
        content = text_pdf_bytes()
        f = SimpleUploadedFile("meta.pdf", content, content_type="application/pdf")
        response = self.client.post("/api/documents/upload", {"file": f, "consent_accepted": "true"})
        doc = UploadedDocument.objects.get(id=response.json()["document_id"])
        self.assertEqual(doc.sha256_hash, hashlib.sha256(content).hexdigest())
        self.assertEqual(doc.file_size, len(content))

    def test_text_pdf_extraction_succeeds(self):
        f = SimpleUploadedFile("t.pdf", text_pdf_bytes(), content_type="application/pdf")
        response = self.client.post("/api/documents/upload", {"file": f, "consent_accepted": "true"})
        doc_id = response.json()["document_id"]
        self.client.post(f"/api/documents/{doc_id}/extract")
        text_resp = self.client.get(f"/api/documents/{doc_id}/extracted-text")
        self.assertEqual(text_resp.status_code, 200)

    def test_extract_endpoint_accepts_trailing_slash(self):
        f = SimpleUploadedFile("slash.pdf", text_pdf_bytes(), content_type="application/pdf")
        response = self.client.post("/api/documents/upload", {"file": f, "consent_accepted": "true"})
        doc_id = response.json()["document_id"]
        extract_resp = self.client.post(f"/api/documents/{doc_id}/extract/")
        self.assertEqual(extract_resp.status_code, 200)

    def test_scanned_pdf_fails_gracefully(self):
        f = SimpleUploadedFile("scan.pdf", scanned_pdf_bytes(), content_type="application/pdf")
        response = self.client.post("/api/documents/upload", {"file": f, "consent_accepted": "true"})
        doc = UploadedDocument.objects.get(id=response.json()["document_id"])
        extract_text(doc)
        doc.refresh_from_db()
        self.assertEqual(doc.status, UploadedDocument.Status.EXTRACTION_FAILED)

    def test_delete_marks_deleted(self):
        f = SimpleUploadedFile("d.pdf", text_pdf_bytes(), content_type="application/pdf")
        response = self.client.post("/api/documents/upload", {"file": f, "consent_accepted": "true"})
        doc_id = response.json()["document_id"]
        delete = self.client.delete(f"/api/documents/{doc_id}")
        self.assertEqual(delete.status_code, 200)
        self.assertEqual(UploadedDocument.objects.get(id=doc_id).status, UploadedDocument.Status.DELETED)

    def test_cannot_access_others_document(self):
        doc = UploadedDocument.objects.create(
            user=self.other,
            original_filename="a.pdf",
            file=SimpleUploadedFile("a.pdf", text_pdf_bytes(), content_type="application/pdf"),
            file_type="pdf",
            file_size=10,
            sha256_hash="a" * 64,
        )
        resp = self.client.get(f"/api/documents/{doc.id}")
        self.assertEqual(resp.status_code, 404)

    def test_extraction_failure_does_not_affect_wallet(self):
        wallet_before = get_wallet(self.user).balance
        f = SimpleUploadedFile("pic.png", b"abc", content_type="image/png")
        response = self.client.post("/api/documents/upload", {"file": f, "consent_accepted": "true"})
        self.client.post(f"/api/documents/{response.json()['document_id']}/extract")
        self.assertEqual(get_wallet(self.user).balance, wallet_before)
