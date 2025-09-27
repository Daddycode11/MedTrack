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
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render
from .models import DetentionInstance
from .filters import PDLFilter

def pdl_list(request):
    """
    List PDLs with filters, consultation counts, and summary groupings.
    """
    detention_instances = (
        DetentionInstance.objects
        .select_related('pdl_profile', 'detention_status', 'detention_reason')
        .annotate(
            # per-row consultation count for display
            consultation_count=Count('pdl_profile__consultation', distinct=True)
        )
    )

    pdl_filter = PDLFilter(request.GET, queryset=detention_instances)
    qs = pdl_filter.qs

    # Overall totals
    total_pdl_rows = qs.count()
    total_consults = qs.aggregate(
        s=Count('pdl_profile__consultation', distinct=True)
    )['s'] or 0

    # By sex (from PDLProfile.sex)
    by_sex = list(
        qs.values('pdl_profile__sex')
          .annotate(
              count=Count('id'),
              consults=Count('pdl_profile__consultation', distinct=True),
          )
          .order_by('-count')
    )
    sex_label = {'M': 'Male', 'F': 'Female', None: 'Unknown', '': 'Unknown'}
    for row in by_sex:
        row['label'] = sex_label.get(row['pdl_profile__sex'], 'Unknown')

    # By detention status (field is "status", not "name")
    by_status = list(
        qs.values('detention_status__id', 'detention_status__status')
          .annotate(
              count=Count('id'),
              consults=Count('pdl_profile__consultation', distinct=True),
          )
          .order_by('-count')
    )
    for row in by_status:
        row['label'] = row.get('detention_status__status') or 'Unspecified'

    # By detention reason (field is "reason")
    by_reason = list(
        qs.values('detention_reason__id', 'detention_reason__reason')
          .annotate(
              count=Count('id'),
              consults=Count('pdl_profile__consultation', distinct=True),
          )
          .order_by('-count')
    )
    for row in by_reason:
        row['label'] = row.get('detention_reason__reason') or 'Unspecified'

    summary = {
        'total_pdl_rows': total_pdl_rows,
        'total_consults': total_consults,
        'by_sex': by_sex,
        'by_status': by_status,
        'by_reason': by_reason,
    }

    # Pagination
    paginator = Paginator(qs, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': pdl_filter,
        'page_obj': page_obj,
        'summary': summary,
    }
    return render(request, 'pdl/pdl_list.html', context=context)

def pdl_profile(request, username):
    """
    View to display the profile of a specific PDL.
    """

    # emulate profile for username = 'johndoe'

    user = get_object_or_404(User, username=username)
    pdl_profile = PDLProfile.objects.get(username=user)
    # fetch the detention instance
    detention_instance = DetentionInstance.objects.filter(pdl_profile=pdl_profile).first()
  
    # Remap to get all the detention instances for the PDL
    detention_instances = DetentionInstance.objects.filter(pdl_profile=pdl_profile)

    # Get consultations for the PDL
    consultations = (
        Consultation.objects
        .filter(pdl_profile=pdl_profile)
        .exclude(status="completed")
    )

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
    

from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import PDLProfile, DetentionInstance
@login_required
def pdl_detention_room_api(request, pk: int):
    """
    Return the latest detention_room_number for the given PDLProfile,
    and try to map it to a Location id (if you have a Location model).
    """
    try:
        pdl = PDLProfile.objects.get(pk=pk)
    except PDLProfile.DoesNotExist:
        raise Http404("PDL not found")

    latest = (
        DetentionInstance.objects
        .filter(pdl_profile=pdl)
        .exclude(detention_room_number__isnull=True)
        .exclude(detention_room_number__exact="")
        .order_by('-detention_start_date', '-created_at')
        .first()
    )

    room_number = latest.detention_room_number if latest else None


    return JsonResponse({
        "room_number": room_number,
    })


# pdl/views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.db import transaction

from django.contrib.auth.models import User
from .models import PDLProfile, DetentionInstance
from .forms import UserForm, PDLProfileForm, DetentionInstanceForm


def edit_pdl(request, pdl_id):
    """
    Edit an existing PDL (User + PDLProfile + latest DetentionInstance) in one page.
    Non-tabbed Bootstrap layout with three sections.
    """
    pdl_profile = get_object_or_404(
        PDLProfile.objects.select_related("username").prefetch_related("detention_instances"),
        pk=pdl_id
    )
    user = pdl_profile.username

    # Current (latest) detention instance or None
    detention_instance = (
        pdl_profile.detention_instances
        .order_by("-detention_start_date", "-created_at")
        .first()
    )

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        pdl_profile_form = PDLProfileForm(request.POST, instance=pdl_profile)
        detention_instance_form = DetentionInstanceForm(request.POST, instance=detention_instance)

        # Save everything atomically
        if user_form.is_valid() and pdl_profile_form.is_valid() and detention_instance_form.is_valid():
            with transaction.atomic():
                user = user_form.save()

                p = pdl_profile_form.save(commit=False)
                p.username = user  # keep link consistent
                p.save()

                di = detention_instance_form.save(commit=False)
                di.pdl_profile = p
                di.save()

            messages.success(request, "PDL details have been updated.")
            return redirect("pdl:pdl_list")
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        user_form = UserForm(instance=user)
        pdl_profile_form = PDLProfileForm(instance=pdl_profile)
        detention_instance_form = DetentionInstanceForm(instance=detention_instance)

    return render(
        request,
        "pdl/edit_pdl.html",
        {
            "pdl_profile": pdl_profile,
            "user_form": user_form,
            "pdl_profile_form": pdl_profile_form,
            "detention_instance_form": detention_instance_form,
        },
    )


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import PDLProfile  # adjust import to your app structure

@require_POST
def delete_pdl(request, pk: int):
    """
    Deletes a PDLProfile by primary key.
    This is triggered from a single modal with a dynamic action URL.
    """
    profile = get_object_or_404(PDLProfile, pk=pk)
    display_name = str(profile)
    profile.delete()
    messages.success(request, f"PDL '{display_name}' was deleted.")
    return redirect("pdl:pdl_list")  # update to your list view name
