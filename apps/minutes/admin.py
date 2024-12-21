from django.contrib import admin
from .models import Minute, ApprovalStep

@admin.register(Minute)
class MinuteAdmin(admin.ModelAdmin):
    list_display = ("title", "approval_chain", "unique_id", "created_at", "is_approved")
    search_fields = ("title", "unique_id")

@admin.register(ApprovalStep)
class ApprovalStepAdmin(admin.ModelAdmin):
    list_display = ("id", "minute", "approver", "step_order", "status")  # Remove 'approved_at'
    list_filter = ("status", "minute__title", "approver__username")
    search_fields = ("minute__title", "approver__username")


