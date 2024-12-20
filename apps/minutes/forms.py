from django import forms
from .models import Minute, ApprovalStep
from django.contrib.auth import get_user_model

User = get_user_model()


class MinuteForm(forms.ModelForm):
    approvers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_staff=True),
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),  # Select2 for a searchable dropdown
        label="Approval Chain (Select Approvers)"
    )

    class Meta:
        model = Minute
        fields = ['title', 'description', 'attachment']  # Fields in the Minute model
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'attachment': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def clean(self):
        """
        Custom validation to ensure the approver list is valid.
        """
        cleaned_data = super().clean()
        approvers = cleaned_data.get('approvers')

        if not approvers:
            raise forms.ValidationError("At least one approver must be selected.")

        # Ensure no duplicates in approvers
        if len(approvers) != len(set(approvers)):
            raise forms.ValidationError("Duplicate approvers are not allowed.")

        return cleaned_data

    def save(self, commit=True):
        """
        Save the Minute instance and create associated ApprovalStep entries.
        """
        minute = super().save(commit=commit)
        if commit:
            approvers = self.cleaned_data.get('approvers')
            if approvers:
                for idx, approver in enumerate(approvers, start=1):
                    ApprovalStep.objects.create(
                        minute=minute,
                        approver=approver,
                        step_order=idx
                    )
        return minute