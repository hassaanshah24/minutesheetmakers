from django.contrib import admin
from .models import Minute, ApprovalStep

@admin.register(Minute)
class MinuteAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('title', 'created_by__username', 'comments')

@admin.register(ApprovalStep)
class ApprovalStepAdmin(admin.ModelAdmin):
    list_display = ('minute', 'approver', 'step_order', 'status', 'approved_at')
    list_filter = ('status',)
    search_fields = ('minute__title', 'approver__username')
