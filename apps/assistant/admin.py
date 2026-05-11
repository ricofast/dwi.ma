from django.contrib import admin

from .models import AIJob, AIResponse, PromptTemplate, SafetyFlag


@admin.register(AIJob)
class AIJobAdmin(admin.ModelAdmin):
    list_display = ("user", "job_type", "provider", "model", "status", "created_at", "completed_at", "error_message")
    list_filter = ("status", "provider", "model", "job_type", "created_at")


admin.site.register(PromptTemplate)
admin.site.register(AIResponse)
admin.site.register(SafetyFlag)
