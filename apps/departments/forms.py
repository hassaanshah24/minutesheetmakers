# departments/forms.py

from django import forms
from .models import Department
from django.contrib.auth import get_user_model

User = get_user_model()

class DepartmentForm(forms.ModelForm):
    head_of_department = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),  # Adjust filter based on your user model
        required=False,
        label="Head of Department"
    )

    class Meta:
        model = Department
        fields = ['name', 'description', 'head_of_department']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'head_of_department': forms.Select(attrs={'class': 'form-control'}),
        }
