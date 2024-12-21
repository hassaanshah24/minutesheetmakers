from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ApprovalChain(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="approval_chains")

    def __str__(self):
        return self.name

class ApprovalStep(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    chain = models.ForeignKey(
        ApprovalChain,
        on_delete=models.CASCADE,
        related_name="approval_steps",
        default=None,  # Specify the default value
        null=True,  # Allow null values temporarily
    )
    approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="approval_chain_steps")
    step_order = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Step {self.step_order}: {self.approver.get_full_name()} ({self.chain.name})"
