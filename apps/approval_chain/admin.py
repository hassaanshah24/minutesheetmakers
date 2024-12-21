from django.contrib import admin
from .models import ApprovalChain, ApprovalStep

@admin.register(ApprovalChain)
class ApprovalChainAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "created_by")

@admin.register(ApprovalStep)
class ApprovalStepAdmin(admin.ModelAdmin):
    list_display = ("chain", "approver", "step_order", "status")
    list_filter = ("status",)
    search_fields = ("chain__name", "approver__username")
