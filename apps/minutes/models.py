from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import datetime
from django.db import transaction

User = get_user_model()


# Helper function to generate unique IDs
def generate_unique_id(department_name=None):
    now = datetime.datetime.now()
    with transaction.atomic():
        latest_minute = Minute.objects.order_by('id').last()
        count = latest_minute.id + 1 if latest_minute else 1
        department_code = department_name or "GEN"
        return f"DHA/DSU/{department_code}/{now.strftime('%m-%y')}/{count:04}"


class Minute(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_minutes')
    is_approved = models.BooleanField(default=False)
    current_step = models.PositiveIntegerField(default=1)
    comments = models.TextField(null=True, blank=True)
    attachment = models.FileField(upload_to='minutes_attachments/', null=True, blank=True)
    unique_id = models.CharField(max_length=20, unique=True, default=generate_unique_id)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            department_name = getattr(self.created_by.profile.department, 'name', "GEN")
            self.unique_id = generate_unique_id(department_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.unique_id} - {self.title} ({'Approved' if self.is_approved else 'Pending'})"

    def progress_approval_chain(self):
        """
        Progresses the approval chain to the next step.
        """
        current_step = self.approval_steps.filter(step_order=self.current_step).first()
        if current_step:
            current_step.status = 'approved'
            current_step.approved_at = now()
            current_step.save()

            next_step = self.approval_steps.filter(step_order=self.current_step + 1).first()
            if next_step:
                self.current_step += 1
            else:
                self.is_approved = True  # If no further steps, mark as approved
        self.save()


class ApprovalStep(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    minute = models.ForeignKey(Minute, on_delete=models.CASCADE, related_name='approval_steps')
    approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_steps')
    step_order = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('minute', 'step_order')
        ordering = ['step_order']

    def __str__(self):
        return f"{self.minute.title} - Step {self.step_order} ({self.get_status_display()})"
