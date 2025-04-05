from django.shortcuts import render, get_object_or_404
from .models import PDLProfile, DetentionInstance
from medications.models import MedicationPrescription
from django.core.paginator import Paginator
from django.db.models import Count, Q
from consultations.models import Consultation
from .filters import PDLFilter

# Create your views here.

def index(request):
    """
    View function for the index page.
    """
    return render(request, "index.html")

def pdl_list(request):
    """
    View function to display a list of PDLs with filters.
    """
    detention_instances = DetentionInstance.objects.select_related('pdl_profile', 'detention_status', 'detention_reason')
    pdl_filter = PDLFilter(request.GET, queryset=detention_instances)

    # Pagination
    paginator = Paginator(pdl_filter.qs, 10)  # Show 10 PDLs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pdl/pdl_list.html', {
        'filter': pdl_filter,
        'page_obj': page_obj,
    })

def pdl_profile(request, pk):
    """
    View to display the profile of a specific PDL.
    """
    # fetch the detention instance
    detention_instance = get_object_or_404(DetentionInstance, pk=pk)
    pdl = get_object_or_404(PDLProfile, pk=detention_instance.pdl_profile.pk)

    # Remap to get all the detention instances for the PDL
    detention_instances = DetentionInstance.objects.filter(pdl_profile=pdl)

    # Get consultations for the PDL
    consultations = Consultation.objects.filter(pdl_profile=pdl)

    # Get medication prescriptions for the PDL
    medication_prescriptions = MedicationPrescription.objects.filter(pdl_profile=pdl)

    context = {
        "pdl": pdl,
        "detention_instances": detention_instances,
        "consultations": consultations,
        "prescriptions": medication_prescriptions,
    }

    return render(request, 'pdl/pdl_profile.html', context=context)