from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Medication, MedicationPrescription

def medication_list(request):
    """
    View function to display a list of medications grouped by medication type.
    """
    medications = Medication.objects.select_related('generic_name__medication_type').annotate(
        prescription_count=Count('medicationprescription')
    )
    grouped_medications = {}
    for medication in medications:
        medication_type = medication.generic_name.medication_type.name
        if medication_type not in grouped_medications:
            grouped_medications[medication_type] = []
        grouped_medications[medication_type].append(medication)

    return render(request, 'medications/medication_list.html', {'grouped_medications': grouped_medications})

def prescription_list(request, medication_id):
    """
    View function to display prescriptions for a specific medication.
    """
    medication = get_object_or_404(Medication, id=medication_id)
    prescriptions = MedicationPrescription.objects.filter(medication=medication)
    return render(request, 'medications/prescription_list.html', {
        'medication': medication,
        'prescriptions': prescriptions
    })
