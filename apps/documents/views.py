from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import UploadedDocument


@login_required
def upload_page(request):
    return render(request, "documents/upload.html")


@login_required
def document_detail(request, document_id):
    document = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    return render(request, "documents/detail.html", {"document": document})


@login_required
def extraction_result(request, document_id):
    document = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    return render(request, "documents/extraction_result.html", {"document": document})
