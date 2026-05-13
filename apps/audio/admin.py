from django.contrib import admin
from apps.audio.models import VoiceNote, TranscriptionJob

@admin.register(VoiceNote)
class VoiceNoteAdmin(admin.ModelAdmin):
    list_display=("user","status","source","created_at")
    list_filter=("status","source","created_at")

@admin.register(TranscriptionJob)
class TranscriptionJobAdmin(admin.ModelAdmin):
    list_display=("voice_note","provider","model","status","created_at","completed_at")
    list_filter=("status","provider","model","created_at")
