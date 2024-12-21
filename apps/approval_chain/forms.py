from django import forms
from .models import ApprovalChain, ApprovalStep
from django.contrib.auth import get_user_model

User = get_user_model()

class ApprovalChainForm(forms.ModelForm):
    class Meta:
        model = ApprovalChain
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class ApprovalStepForm(forms.ModelForm):
    approver = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = ApprovalStep
        fields = ["approver", "step_order"]
