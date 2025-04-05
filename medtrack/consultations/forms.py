from django import forms
from .models import Consultation
from pdl.models import PDLProfile
from consultations.models import Physician, ConsultationLocation, ConsultationReason

class ScheduleConsultationForm(forms.ModelForm):
    """
    Form for scheduling a consultation.
    """
    class Meta:
        model = Consultation
        fields = [
            'pdl_profile',
            'physician',
            'location',
            'reason',
            'consultation_date_date_only',
            'consultation_time_block',
            'is_an_emergency',
            'notes',
        ]
        widgets = {
            'pdl_profile': forms.Select(attrs={'class': 'form-select'}),
            'physician': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Select(attrs={'class': 'form-select'}),
            'consultation_date_date_only': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'consultation_time_block': forms.Select(attrs={'class': 'form-select'}),
            'is_an_emergency': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }