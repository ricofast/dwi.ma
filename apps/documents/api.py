from datetime import datetime
from uuid import UUID

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ninja import File, Form, Router
from ninja.files import UploadedFile
from ninja.errors import HttpError
from pydantic import BaseModel

from apps.accounts.auth import require_auth
from apps.documents.models import UploadedDocument
from apps.documents.services.extraction import calculate_file_hash, extract_text, validate_document_file

router = Router(tags=["documents"])


class DocumentOut(BaseModel):
    document_id: UUID
    status: str
    filename: str
    file_type: str
    file_size: int


@router.post("/documents/upload", response=DocumentOut)
def upload_document(request, file: UploadedFile = File(...), consent_accepted: bool = Form(False), source: str = Form("pwa")):
    require_auth(request)
    if not consent_accepted:
        raise HttpError(400, "Privacy consent is required")
    try:
        file_type = validate_document_file(file)
    except ValidationError as exc:
        raise HttpError(400, "; ".join(exc.messages))

    document = UploadedDocument.objects.create(
        user=request.user,
        original_filename=file.name,
        file=file,
        file_type=file_type,
        file_size=file.size,
        sha256_hash=calculate_file_hash(file),
        source=source,
        status=UploadedDocument.Status.UPLOADED,
    )
    return DocumentOut(
        document_id=document.id,
        status=document.status,
        filename=document.original_filename,
        file_type=document.file_type,
        file_size=document.file_size,
    )


@router.get("/documents/{document_id}")
def get_document(request, document_id: UUID):
    require_auth(request)
    doc = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    return {
        "document_id": doc.id,
        "status": doc.status,
        "filename": doc.original_filename,
        "file_type": doc.file_type,
        "file_size": doc.file_size,
        "source": doc.source,
        "deleted_at": doc.deleted_at,
        "created_at": doc.created_at,
    }


def _extract_document(request, document_id: UUID):
    require_auth(request)
    doc = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    doc.status = UploadedDocument.Status.EXTRACTING
    doc.save(update_fields=["status", "updated_at"])
    extract_text(doc)
    doc.refresh_from_db()
    return {"document_id": str(doc.id), "status": doc.status}


@router.post("/documents/{document_id}/extract")
@router.post("/documents/{document_id}/extract/")
@router.get("/documents/{document_id}/extract")
@router.get("/documents/{document_id}/extract/")
def extract_document(request, document_id: UUID):
    return _extract_document(request, document_id)


@router.get("/documents/{document_id}/extracted-text")
def get_extracted_text(request, document_id: UUID):
    require_auth(request)
    doc = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    if not hasattr(doc, "extracted_text"):
        raise HttpError(404, "Extracted text not available")
    return {
        "document_id": str(doc.id),
        "status": doc.status,
        "extraction_method": doc.extracted_text.extraction_method,
        "text": doc.extracted_text.text,
        "page_count": doc.extracted_text.page_count,
    }


@router.delete("/documents/{document_id}")
def delete_document(request, document_id: UUID):
    require_auth(request)
    doc = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    storage = doc.file.storage
    file_name = doc.file.name
    if file_name and storage.exists(file_name):
        storage.delete(file_name)
    doc.mark_deleted()
    return {"status": "deleted", "deleted_at": datetime.utcnow().isoformat()}

from apps.assistant.models import AIJob
from apps.documents.models import DocumentAnalysis
from apps.documents.tasks import explain_document_task
from apps.wallet.services import can_spend


class ExplainIn(BaseModel):
    output_language: str = "darija_arabic"


@router.post("/documents/{document_id}/explain")
@router.post("/documents/{document_id}/explain/")
@router.get("/documents/{document_id}/explain")
@router.get("/documents/{document_id}/explain/")
def explain_doc(request, document_id: UUID, payload: ExplainIn):
    require_auth(request)
    doc = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    if not hasattr(doc, "extracted_text") or doc.status != UploadedDocument.Status.EXTRACTED:
        raise HttpError(400, "Document extraction is required")
    if not can_spend(request.user, 1):
        raise HttpError(402, "Insufficient credits")
    job = AIJob.objects.create(user=request.user, job_type=AIJob.JobType.DOCUMENT_EXPLANATION, provider="", model="", status=AIJob.Status.QUEUED, input_hash="", input_preview="", prompt_version="")
    explain_document_task.delay(str(document_id), str(request.user.id))
    return {"job_id": str(job.id), "document_id": str(document_id), "status": "queued"}


@router.get("/documents/{document_id}/analysis")
def get_analysis(request, document_id: UUID):
    require_auth(request)
    doc = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    analysis = DocumentAnalysis.objects.filter(document=doc).first()
    if not analysis:
        return {"status": doc.status}
    return {"status": "completed", "document_type": analysis.document_type, "summary_darija": analysis.summary_darija, "important_points": analysis.important_points_json, "extracted_entities": analysis.extracted_entities_json, "unclear_points": analysis.unclear_points_json, "next_steps": analysis.next_steps_json, "disclaimer": analysis.disclaimer_darija, "full_answer": analysis.full_response_text}


@router.get("/assistant/jobs/{job_id}")
def get_job_status(request, job_id: UUID):
    require_auth(request)
    job = get_object_or_404(AIJob, id=job_id, user=request.user)
    return {"job_id": str(job.id), "status": job.status, "result_available": bool(job.result_json), "error_message": job.error_message or ""}
