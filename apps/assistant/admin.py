from django.contrib import admin

from .models import AIJob, AIResponse, PromptTemplate, SafetyFlag, TextExplanation, MessageGeneration


@admin.register(AIJob)
class AIJobAdmin(admin.ModelAdmin):
    list_display = ("user", "job_type", "provider", "model", "status", "created_at", "completed_at", "error_message")
    list_filter = ("status", "provider", "model", "job_type", "created_at")


admin.site.register(PromptTemplate)
admin.site.register(AIResponse)
admin.site.register(SafetyFlag)


@admin.register(TextExplanation)
class TextExplanationAdmin(admin.ModelAdmin):
    list_display = ("user", "ai_job", "detected_text_type", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")


@admin.register(MessageGeneration)
class MessageGenerationAdmin(admin.ModelAdmin):
    list_display=("user","ai_job","target_format","tone","created_at")
    list_filter=("target_format","tone","created_at")
