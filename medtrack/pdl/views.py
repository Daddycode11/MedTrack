from django.shortcuts import render
from .models import PDLProfile
from django.core.paginator import Paginator

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

    # Fetch all PDL profiles from the database
    pdl_profiles = PDLProfile.objects.all()

    # Set up pagination with 10 items per page
    paginator = Paginator(pdl_profiles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }

    return render(request, "pdl/pdl_list.html", context)