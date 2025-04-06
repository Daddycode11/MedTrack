from django.shortcuts import render, get_object_or_404, redirect
from .models import PDLProfile, DetentionInstance
from medications.models import MedicationPrescription
from django.core.paginator import Paginator
from django.db.models import Count, Q
from consultations.models import Consultation
from .filters import PDLFilter
from django.contrib.auth.models import User
from .forms import UserForm, PDLProfileForm, DetentionInstanceForm

# Create your views here.

def index(request):
    """
    View function for the index page.
    """
    return render(request, "index.html")

def pdl_list(request):
    """
    View function to display a list of PDLs with filters and consultation counts.
    """
    # Fetch detention instances and annotate with consultation counts
    detention_instances = DetentionInstance.objects.select_related(
        'pdl_profile', 'detention_status', 'detention_reason'
    ).annotate(
        consultation_count=Count(
            'pdl_profile__consultation',
            filter=Q(pdl_profile__consultation__status='scheduled')
        )
    )

    # Apply filters
    pdl_filter = PDLFilter(request.GET, queryset=detention_instances)

    # Pagination
    paginator = Paginator(pdl_filter.qs, 10)  # Show 10 PDLs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pdl/pdl_list.html', {
        'filter': pdl_filter,
        'page_obj': page_obj,
    })

def pdl_profile(request):
    """
    View to display the profile of a specific PDL.
    """

    # emulate profile for username = 'johndoe'

    user = User.objects.get(username='johndoe')
    pdl_profile = PDLProfile.objects.get(username=user)
    # fetch the detention instance
    detention_instance = DetentionInstance.objects.filter(pdl_profile=pdl_profile).first()
  
    # Remap to get all the detention instances for the PDL
    detention_instances = DetentionInstance.objects.filter(pdl_profile=pdl_profile)

    # Get consultations for the PDL
    consultations = Consultation.objects.filter(pdl_profile=pdl_profile)

    # Get medication prescriptions for the PDL
    medication_prescriptions = MedicationPrescription.objects.filter(pdl_profile=pdl_profile)

    context = {
        "pdl": pdl_profile,
        "detention_instance": detention_instance,
        "detention_instances": detention_instances,
        "consultations": consultations,
        "prescriptions": medication_prescriptions,
    }

    return render(request, 'pdl/pdl_profile.html', context=context)


def pdl_profile_by_id(request, pk):
    """
    View to display the profile of a specific PDL.
    """

    # emulate profile for username = 'johndoe'

    detention_instance = get_object_or_404(DetentionInstance, pk=pk)
    pdl_profile = detention_instance.pdl_profile

    # Remap to get all the detention instances for the PDL
    detention_instances = DetentionInstance.objects.filter(pdl_profile=pdl_profile)

    # Get consultations for the PDL
    consultations = Consultation.objects.filter(pdl_profile=pdl_profile)

    # Get medication prescriptions for the PDL
    medication_prescriptions = MedicationPrescription.objects.filter(pdl_profile=pdl_profile)

    context = {
        "pdl": pdl_profile,
        "detention_instance": detention_instance,
        "detention_instances": detention_instances,
        "consultations": consultations,
        "prescriptions": medication_prescriptions,
    }

    return render(request, 'pdl/pdl_profile.html', context=context)

def add_pdl(request):
    """
    View to add a new PDL with detention instance details.
    """
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        pdl_profile_form = PDLProfileForm(request.POST)
        detention_instance_form = DetentionInstanceForm(request.POST)
        if user_form.is_valid() and pdl_profile_form.is_valid() and detention_instance_form.is_valid():
            # Save the User first
            user = user_form.save()

            # Save the PDLProfile and associate it with the User
            pdl_profile = pdl_profile_form.save(commit=False)
            pdl_profile.username = user
            pdl_profile.save()

            # Save the DetentionInstance and associate it with the PDLProfile
            detention_instance = detention_instance_form.save(commit=False)
            detention_instance.pdl_profile = pdl_profile
            detention_instance.save()

            return redirect('pdl:pdl_list')  # Redirect to the PDL list after saving
    else:
        user_form = UserForm()
        pdl_profile_form = PDLProfileForm()
        detention_instance_form = DetentionInstanceForm()

    return render(request, 'pdl/add_pdl.html', {
        'user_form': user_form,
        'pdl_profile_form': pdl_profile_form,
        'detention_instance_form': detention_instance_form,
    })