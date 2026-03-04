from django import forms
from .models import Medication, MedicationInventory, InventoryTransaction, MedicationPrescription

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'generic_name', 'dosage_form', 'strength', 'route_of_administration', 'manufacturer']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand Name'}),
            'generic_name': forms.Select(attrs={'class': 'form-select'}),
            'dosage_form': forms.Select(attrs={'class': 'form-select'}),
            'strength': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500mg'}),
            'route_of_administration': forms.Select(attrs={'class': 'form-select'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manufacturer Name'}),
        }

class MedicationInventoryForm(forms.ModelForm):
    class Meta:
        model = MedicationInventory
        fields = ['quantity', 'reorder_level', 'expiration_date', 'location']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'value': '10'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Storage Location'}),
        }

class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = MedicationInventory
        fields = ['quantity', 'reorder_level', 'expiration_date', 'location']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction
        fields = ['transaction_type', 'quantity_change', 'notes']
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity_change': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class MedicationPrescriptionForm(forms.ModelForm):
    class Meta:
        model = MedicationPrescription
        # Inalis ang 'status' dito para maging automatic ang calculation
        fields = [
            'pdl_profile',
            'medication',
            'dosage',
            'frequency',
            'duration',
            'prescribed_by',
            'quantity_prescribed',
            'quantity_dispensed',
        ]
        widgets = {
            'pdl_profile': forms.Select(attrs={'class': 'form-select'}),
            'medication': forms.Select(attrs={'class': 'form-select'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500mg'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3 times a day'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 7 days'}),
            'prescribed_by': forms.Select(attrs={'class': 'form-select'}),
            'quantity_prescribed': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'quantity_dispensed': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'value': '0'}),
            # Tinanggal ang status widget
        }