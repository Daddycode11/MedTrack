from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django_filters.views import FilterView
from .models import Medication, MedicationPrescription
from .filters import MedicationFilter

def medication_list(request):
    """
    View function to display a list of medications grouped by medication type with filters.
    """
    medications = Medication.objects.select_related('generic_name__medication_type').annotate(
        prescription_count=Count('medicationprescription')
    )
    medication_filter = MedicationFilter(request.GET, queryset=medications)

    grouped_medications = {}
    for medication in medication_filter.qs:
        medication_type = medication.generic_name.medication_type.name
        if medication_type not in grouped_medications:
            grouped_medications[medication_type] = []
        grouped_medications[medication_type].append(medication)

    return render(request, 'medications/medication_list.html', {
        'grouped_medications': grouped_medications,
        'filter': medication_filter,
    })

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


# pharmacy/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import MedicationPrescriptionForm

@login_required
def prescription_create(request):
    if request.method == "POST":
        form = MedicationPrescriptionForm(request.POST)
        if form.is_valid():
            presc = form.save()
            messages.success(request, "Prescription recorded successfully.")
            return redirect(reverse("medications:prescription_detail", args=[presc.id]))
        messages.error(request, "Please correct the errors below.")
    else:
        form = MedicationPrescriptionForm()
    return render(request, "medications/prescription_form.html", {"form": form})

# pharmacy/views.py (add this simple placeholder)
from django.shortcuts import get_object_or_404
from .models import MedicationPrescription

@login_required
def prescription_detail(request, pk):
    obj = get_object_or_404(MedicationPrescription, pk=pk)
    return render(request, "medications/prescription_detail.html", {"obj": obj})
