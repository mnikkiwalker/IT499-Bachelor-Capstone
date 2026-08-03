from django import forms
from .models import IntakeForm


class IntakeFormForm(forms.ModelForm):

    class Meta:
        model = IntakeForm
        fields = [
            "reason_for_visit",
            "symptoms",
            "current_medications",
            "allergies",
            "consent",
        ]
        widgets = {
            "symptoms": forms.Textarea(attrs={"rows": 3}),
            "current_medications": forms.Textarea(attrs={"rows": 2}),
            "allergies": forms.Textarea(attrs={"rows": 2}),
        }
        