# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


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

    def save(self, *args, **kwargs):
        """
        Synchronize role with is_superuser and is_staff flags,
        but bypass this logic for explicitly created superusers.
        """
        if self.is_superuser and not self.role:
            # For superusers, set the role to 'Superuser' only if not already set
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

        # Ensure consistency for superusers
        if self.is_superuser:
            self.is_staff = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.role if self.role else 'No Role Assigned'}"
