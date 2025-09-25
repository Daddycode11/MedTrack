# pharmacy/forms.py
from django import forms
from .models import MedicationPrescription, Medication
from pdl.models import PDLProfile
from consultations.models import Physician

class MedicationPrescriptionForm(forms.ModelForm):
    pdl_profile = forms.ModelChoiceField(
        queryset=PDLProfile.objects.select_related('username').order_by('username__last_name', 'username__first_name'),
        label="Patient (PDL Profile)"
    )
    medication = forms.ModelChoiceField(
        queryset=Medication.objects.select_related('generic_name').order_by('name'),
        label="Medication"
    )
    prescribed_by = forms.ModelChoiceField(
        queryset=Physician.objects.select_related('username').order_by('username__last_name', 'username__first_name'),
        label="Prescribing Physician"
    )

    class Meta:
        model = MedicationPrescription
        fields = ["pdl_profile", "medication", "dosage", "frequency", "duration", "prescribed_by"]
        widgets = {
            "pdl_profile": forms.Select(attrs={"class": "form-select"}),
            "medication": forms.Select(attrs={"class": "form-select"}),
            "dosage": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., 500 mg"}),
            "frequency": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., twice daily"}),
            "duration": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., 7 days"}),
            "prescribed_by": forms.Select(attrs={"class": "form-select"}),
        }
        help_texts = {
            "dosage": "Strength per administration (e.g., 500 mg).",
            "frequency": "How often (e.g., BID, every 8 hours, once daily).",
            "duration": "Total course (e.g., 7 days, 10 doses).",
        }

    def clean(self):
        cleaned = super().clean()
        # Optional: light normalization to keep entries consistent
        freq = cleaned.get("frequency") or ""
        cleaned["frequency"] = freq.strip()
        duration = cleaned.get("duration") or ""
        cleaned["duration"] = duration.strip()

        # Example guardrails: basic sanity checks
        if not cleaned.get("dosage"):
            self.add_error("dosage", "Please specify the dosage.")
        if not cleaned.get("frequency"):
            self.add_error("frequency", "Please specify the frequency.")
        if not cleaned.get("duration"):
            self.add_error("duration", "Please specify the duration.")
        return cleaned
