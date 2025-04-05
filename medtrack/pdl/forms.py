from django import forms
from .models import PDLProfile, DetentionInstance, DetentionStatus, DetentionReason
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    """
    Form for creating a new User.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class PDLProfileForm(forms.ModelForm):
    """
    Form for creating a new PDLProfile.
    """
    class Meta:
        model = PDLProfile
        fields = ['phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DetentionInstanceForm(forms.ModelForm):
    """
    Form for creating a new DetentionInstance.
    """
    class Meta:
        model = DetentionInstance
        fields = ['detention_status', 'detention_reason', 'detention_term_length', 'detention_start_date', 'detention_end_date', 'notes']
        widgets = {
            'detention_status': forms.Select(attrs={'class': 'form-select'}),
            'detention_reason': forms.Select(attrs={'class': 'form-select'}),
            'detention_term_length': forms.NumberInput(attrs={'class': 'form-control'}),
            'detention_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'detention_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }