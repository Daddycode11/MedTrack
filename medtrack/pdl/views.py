from django.shortcuts import render, get_object_or_404
from .models import PDLProfile, DetentionInstance
from django.core.paginator import Paginator
from django.db.models import Count, Q

# Create your views here.

def index(request):
    """
    View function for the index page.
    """
    return render(request, "index.html")

def pdl_list(request):
    """
    View function for the PDL list page with pagination.
    """

    # Fetch all PDL profiles with the count of scheduled consultations
    pdl_profiles = DetentionInstance.objects.annotate(
        scheduled_consultations_count=Count(
            'pdl_profile__consultation',
            filter=Q(pdl_profile__consultation__status="scheduled")
        )
    ).order_by("pdl_profile__username__last_name")

    # Set up pagination
    paginator = Paginator(pdl_profiles, 10)  # Show 10 profiles per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Render the template with the paginated profiles
    context = {
        "page_obj": page_obj,
    }

    return render(request, "pdl/pdl_list.html", context)

from consultations.models import Consultation

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



    context = {
        "pdl": pdl,
        "detention_instances": detention_instances,
        "consultations": consultations,
    }

    return render(request, 'pdl/pdl_profile.html', context=context)