from django.db import models
from django.db import transaction
import datetime
from django.contrib.auth import get_user_model
from approval_chain.models import ApprovalChain

# Fetch the custom user model
User = get_user_model()

def generate_unique_id(user):
    """
    Generates a unique ID for a minute based on the department, current date, and a counter.
    """
    now = datetime.datetime.now()
    department_name = user.department.name if user.department else "GEN"

    with transaction.atomic():
        latest_minute = Minute.objects.order_by('id').last()
        count = latest_minute.id + 1 if latest_minute else 1
        return f"DHA/DSU/{department_name}/{now.strftime('%m-%y')}/{count:04}"


class Minute(models.Model):
    """
    Represents a minute created by a user.
    """
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]
    approval_chain = models.ForeignKey(
        ApprovalChain,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="minutes"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    attachment = models.FileField(upload_to='minutes_attachments/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_minutes')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_approved = models.BooleanField(default=False)
    current_step = models.PositiveIntegerField(default=1)
    comments = models.TextField(blank=True, null=True)
    unique_id = models.CharField(max_length=50, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = generate_unique_id(self.created_by)
        super().save(*args, **kwargs)

        # Automatically create approval steps if approval_chain is set
        if self.approval_chain and not self.approval_steps.exists():
            for step in self.approval_chain.approval_steps.all():
                ApprovalStep.objects.create(
                    minute=self,
                    approver=step.approver,
                    step_order=step.step_order,
                    status="pending" if step.step_order == 1 else "pending",
                )

    def archive(self):
        """
        Archive the minute after approval or rejection.
        """
        archived_data = {
            'title': self.title,
            'description': self.description,
            'created_by': self.created_by,
            'created_at': self.created_at,
            'status': self.status,
            'comments': self.comments,
        }
        ArchivedMinute.objects.create(**archived_data)
        self.delete()  # Delete the minute after archiving


class ApprovalStep(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    minute = models.ForeignKey(Minute, on_delete=models.CASCADE, related_name="approval_steps")
    approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="minute_approval_steps")  # Unique related_name
    step_order = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.minute.title} - Step {self.step_order} ({self.status})"



class ArchivedMinute(models.Model):
    """
    Stores all minutes after approval or rejection for archival purposes.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='archived_minutes')
    created_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Minute.STATUS_CHOICES)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Archived: {self.title} - {self.status}"
