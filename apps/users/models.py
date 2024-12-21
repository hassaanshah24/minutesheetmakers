from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    """
    Represents a department within the organization.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser with additional fields.
    """
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Superuser', 'Superuser'),
        ('Faculty', 'Faculty'),
    ]
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")

    def save(self, *args, **kwargs):
        """
        Synchronize role with is_superuser and is_staff flags,
        but bypass this logic for explicitly created superusers.
        """
        if self.is_superuser and not self.role:
            self.role = 'Superuser'

        if not self.is_superuser:  # Only apply role logic for non-superusers
            if self.role == 'Superuser':
                self.is_superuser = True
                self.is_staff = True
            elif self.role == 'Admin':
                self.is_staff = True
                self.is_superuser = False
            else:
                self.is_staff = False
                self.is_superuser = False

        if self.is_superuser:
            self.is_staff = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.role if self.role else 'No Role Assigned'}"
