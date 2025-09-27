from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django_filters.views import FilterView
from .models import Medication, MedicationPrescription
from .filters import MedicationFilter
# medications/views.py
from collections import OrderedDict
from django.db.models import Q, Count
from django.shortcuts import render
from .models import MedicationPrescription

def medication_list(request):
    """
    Show CURRENT prescriptions grouped by PDL (not by medication).
    Optional search (?q=) across PDL name/username and medication.
    """
    q = (request.GET.get("q") or "").strip()

    qs = (
        MedicationPrescription.objects
        .select_related(
            "pdl_profile__username",
            "medication__generic_name",
            "prescribed_by",
        )
        .order_by(
            "pdl_profile__username__last_name",
            "pdl_profile__username__first_name",
            "medication__name",
        )
    )

    if q:
        qs = qs.filter(
            Q(pdl_profile__username__first_name__icontains=q) |
            Q(pdl_profile__username__last_name__icontains=q) |
            Q(pdl_profile__username__username__icontains=q) |
            Q(medication__name__icontains=q) |
            Q(medication__generic_name__name__icontains=q)
        )

    # Group by PDL
    grouped = OrderedDict()
    for rx in qs:
        key = rx.pdl_profile_id
        if key not in grouped:
            grouped[key] = {
                "pdl": rx.pdl_profile,
                "items": [],
            }
        grouped[key]["items"].append(rx)

    totals = {
        "pdl_count": len(grouped),
        "rx_count": qs.count(),
    }

    return render(request, "medications/medication_list.html", {
        "grouped_by_pdl": grouped,   # OrderedDict of {pdl_id: {"pdl": PDLProfile, "items": [MedicationPrescription,...]}}
        "q": q,
        "totals": totals,
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


# medications/views.py
import re
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import MedicationPrescription

def _clean(s: str) -> str:
    """Collapse whitespace and strip pipes so the barcode is parse-safe."""
    if s is None:
        return ""
    return re.sub(r"\s+", " ", str(s)).replace("|", "/").strip()

def prescription_printable(request, pk: int):
    rx = get_object_or_404(MedicationPrescription.objects.select_related(
        "pdl_profile__username", "medication__generic_name", "prescribed_by"
    ), pk=pk)

    now = timezone.localtime()
    # Pipe-delimited, deterministic order. Keep short fields first for scanners.
    barcode_payload = "|".join([
        f"RX{rx.pk}",
        f"PDL{rx.pdl_profile.pk}",
        f"MED{rx.medication.pk}",
        _clean(rx.medication.name),
        _clean(rx.dosage),
        _clean(rx.frequency),
        _clean(rx.duration),
        f"DR{rx.prescribed_by.pk}",
        now.strftime("%Y%m%d"),  # issue date
    ])

    return render(request, "medications/prescription_print.html", {
        "rx": rx,
        "now": now,
        "barcode_payload": barcode_payload,
    })


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import MedicationPrescription  # adjust if your model name differs

@require_POST
def prescription_delete(request, pk: int):
    rx = get_object_or_404(MedicationPrescription, pk=pk)
    label = f"{rx.pdl} — {rx.medication.name}" if getattr(rx, "pdl", None) else str(rx)
    rx.delete()
    messages.success(request, f"Prescription '{label}' was deleted.")
    return redirect("medications:medication_list")
