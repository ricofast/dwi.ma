from datetime import timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.audio.models import VoiceNote

class Command(BaseCommand):
    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=settings.AUDIO_ORIGINAL_RETENTION_DAYS)
        for v in VoiceNote.objects.filter(created_at__lt=cutoff, deleted_at__isnull=True):
            if v.audio_file and v.audio_file.name and v.audio_file.storage.exists(v.audio_file.name):
                v.audio_file.storage.delete(v.audio_file.name)
            if settings.DELETE_TRANSCRIPT_ON_AUDIO_DELETE:
                for t in v.transcription_jobs.all():
                    t.transcript = ''
                    t.save(update_fields=['transcript', 'updated_at'])
