from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from datetime import date, timedelta
import datetime as dt
import calendar

from .models import (
    Consultation,
    Physician,
    ConsultationLocation,
    ConsultationReason,
    ConsultationTimeBlock,
)
from .forms import ScheduleConsultationForm
from pdl.models import PDLProfile


def consultation_calendar(request, consultations):
    """
    Generates a calendar view for consultations within a specified month and year.
    Args:
        request (HttpRequest): The HTTP request object containing optional 'year' and 'month' 
            query parameters to specify the calendar's year and month. Defaults to the current 
            year and month if not provided.
        consultations (QuerySet): A queryset of consultation objects, each containing a 
            `consultation_date_date_only` attribute representing the date of the consultation.
    Returns:
        dict: A context dictionary containing the following keys:
            - 'calendar_data' (list): A list of weeks, where each week is a list of dictionaries 
              representing days. Each day dictionary contains:
                - 'day' (int or None): The day of the month, or None for days outside the current month.
                - 'weekday' (int): The weekday index (0=Monday, 6=Sunday).
                - 'consultations' (list): A list of consultations scheduled for that day.
            - 'year' (int): The year of the calendar.
            - 'month' (int): The month of the calendar.
            - 'month_name' (str): The full name of the month.
            - 'prev_month' (int): The previous month (1-12).
            - 'prev_year' (int): The year corresponding to the previous month.
            - 'next_month' (int): The next month (1-12).
            - 'next_year' (int): The year corresponding to the next month.
    """
   
    # Prepare data for the calendar
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    if year < 1 or month < 1 or month > 12:
        messages.error(request, "Invalid year or month provided. Defaulting to the current date.")
        year, month = today.year, today.month

    # Create a calendar object
    cal = calendar.Calendar()
    month_days = cal.itermonthdays2(year, month)  # Returns (day, weekday) tuples

    # Map consultations to their respective dates
    consultation_map = {}
    for consultation in consultations:
        consultation_date = consultation.consultation_date_date_only
        if consultation_date.year == year and consultation_date.month == month:
            consultation_map.setdefault(consultation_date.day, []).append(consultation)

    # Prepare the calendar data
    calendar_data = []
    for day, weekday in month_days:
        if day == 0:  # Skip days outside the current month
            calendar_data.append({'day': None, 'weekday': weekday, 'consultations': []})
        else:
            calendar_data.append({
                'day': day,
                'weekday': weekday,
                'consultations': consultation_map.get(day, [])
            })

    # Group calendar_data by week
    weeks = []
    week = []
    for day_data in calendar_data:
        week.append(day_data)
        if len(week) == 7:  # A week has 7 days
            weeks.append(week)
            week = []
    if week:  # Add any remaining days to the last week
        weeks.append(week)
    calendar_data = weeks 

    # Render the template
    context = {
        'calendar_data': calendar_data,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'prev_month': (month - 1) if month > 1 else 12,
        'prev_year': year if month > 1 else year - 1,
        'next_month': (month + 1) if month < 12 else 1,
        'next_year': year if month < 12 else year + 1
    }

    return context


def all_consultations(request):
    """
    Handles the retrieval and display of all consultations.

    This view fetches all consultation records from the database, 
    prepares the calendar data for the consultations, and renders 
    the consultation calendar template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered consultation calendar template 
        with the context containing consultation data.
    """

    # Fetch all consultations
    consultations = Consultation.objects.all()

    # Get the calendar data
    context = consultation_calendar(request, consultations)

    # Render the template
    return render(request, "consultations/consultation_calendar.html", context)

def consultations_by_physician(request, physician_id):
    """
    Handles the retrieval and display of consultations for a specific physician.

    Args:
        request (HttpRequest): The HTTP request object.
        physician_id (int): The ID of the physician whose consultations are to be retrieved.

    Returns:
        HttpResponse: A rendered HTML page displaying the consultation calendar for the specified physician.

    Raises:
        Http404: If no Physician object with the given ID is found.

    This view fetches all consultations associated with the specified physician,
    prepares the data for a consultation calendar, and renders the corresponding template.
    """

    physician = get_object_or_404(Physician, id=physician_id)
    # Fetch consultations for the specified physician
    consultations = Consultation.objects.filter(physician=physician)

    # Get the calendar data
    context = consultation_calendar(request, consultations)

    # Render the template
    return render(request, "consultations/consultation_calendar.html", context)

def doctor_dashboard(request):
    """
    Displays the doctor's dashboard with relevant information.

    This view function retrieves the physician with the username 'jessicaadams'
    and fetches the next three upcoming consultations for that physician. The
    consultations are filtered to include only those scheduled for today or later
    and are sorted by date and time.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML template for the doctor's dashboard.

    Context:
        physician (Physician): The physician object for 'jessicaadams'.
        upcoming_consultations (QuerySet): A queryset containing up to three
            upcoming consultations for the physician, sorted by date and time.
    """
    
    # Emulate view by fetching 'jessicaadams' physician
    physician = get_object_or_404(Physician, username__username='jessicaadams')

    # Fetch the next three upcoming consultations for the physician
    upcoming_consultations = Consultation.objects.filter(
        physician=physician,
        consultation_date_date_only__gte=date.today(),
        status="scheduled"
    ).order_by('consultation_date_date_only', 'consultation_time_block')[:3]

    context = {
        'physician': physician,
        'upcoming_consultations': upcoming_consultations,
    }

    # Render the template
    return render(request, "consultations/doctor_dashboard.html", context)

def schedule_consultation(request):
    """
    Handle the scheduling of a consultation.

    This view processes both GET and POST requests. For a GET request, it 
    initializes an empty `ScheduleConsultationForm` and renders the 
    consultation scheduling page. For a POST request, it validates the 
    submitted form data, saves the consultation if the form is valid, and 
    redirects the user to the consultation calendar.

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
        about the request.

    Returns:
        HttpResponse: Renders the consultation scheduling page with the form 
        for GET requests or redirects to the consultation calendar for valid 
        POST requests.
    """

    if request.method == 'POST':
        form = ScheduleConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consultations:consultation_calendar')  # Redirect to the consultation list after saving
    else:
        form = ScheduleConsultationForm()

    return render(request, 'consultations/schedule_consultation.html', {'form': form})

def cancel_consultation(request, consultation_id):
    """
    Handles the cancellation of a consultation.
    This view retrieves a consultation by its ID and allows the user to cancel it.
    If the request method is POST, the consultation's status is updated to 'canceled',
    and a success message is displayed to the user. The user is then redirected to
    the consultation calendar. If the request method is not POST, the cancellation
    confirmation page is rendered.
    Args:
        request (HttpRequest): The HTTP request object.
        consultation_id (int): The ID of the consultation to be canceled.
    Returns:
        HttpResponse: Renders the cancellation confirmation page if the request
        method is not POST. Redirects to the consultation calendar if the
        consultation is successfully canceled.
    """
  
    consultation = get_object_or_404(Consultation.objects.select_related('physician'), id=consultation_id)

    if request.method == 'POST':
        # Mark the consultation as canceled
        consultation.status = Consultation.Status.CANCELED  # Use the appropriate constant or enum for 'canceled'
        consultation.save()

        # Add a success message
        messages.success(request, f"Consultation with {consultation.physician} on {consultation.consultation_date_date_only} has been canceled.")
        return redirect('consultations:consultation_calendar')

    return render(request, 'consultations/cancel_consultation.html', {'consultation': consultation})

def reschedule_consultation(request, consultation_id):
    """
    Handle the rescheduling of a consultation.

    This view retrieves a consultation by its ID and allows the user to reschedule it
    by submitting a form. If the form submission is valid, the consultation is updated
    and the user is redirected to the consultation calendar. If the request is not a POST,
    the form is pre-filled with the current consultation details.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        consultation_id (int): The ID of the consultation to be rescheduled. 
            Expected to be a positive integer.

    Returns:
        HttpResponse: Renders the reschedule consultation page with the form if the request
        is not a POST, or redirects to the consultation calendar upon successful form submission.

    Raises:
        Http404: If the consultation with the given ID does not exist.

    Template:
        consultations/reschedule_consultation.html

    Context:
        form (ScheduleConsultationForm): The form for scheduling the consultation.
        consultation (Consultation): The consultation object being rescheduled.
    """

    consultation = get_object_or_404(Consultation, id=consultation_id)

    if request.method == 'POST':
        form = ScheduleConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            form.save()
            messages.success(request, f"Consultation with {consultation.physician} has been rescheduled.")
            return redirect('consultations:consultation_calendar')
    else:
        form = ScheduleConsultationForm(instance=consultation)

    return render(request, 'consultations/reschedule_consultation.html', {'form': form, 'consultation': consultation})

def create_consultation(request):
    if request.method == 'POST':
        try:
            # Extract and parse form data
            date_str = request.POST.get('date')
            time_block = request.POST.get('time')  # This will now be the enum name
            
            # Convert date string to date object
            consultation_date = dt.datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Validate the time block
            if not hasattr(ConsultationTimeBlock, time_block):
                raise ValueError(f'Invalid time block selected: {time_block}')

            # Get related objects
            pdl = get_object_or_404(PDLProfile, id=request.POST.get('pdl'))
            location = get_object_or_404(ConsultationLocation, id=request.POST.get('location'))
            physician = get_object_or_404(Physician, id=request.POST.get('physician'))
            reason = get_object_or_404(ConsultationReason, id=request.POST.get('reason'))
            is_an_emergency = request.POST.get('is_an_emergency') == 'on'
            notes = request.POST.get('notes')

            # Create and save the consultation
            Consultation.objects.create(
                consultation_date_date_only=consultation_date,
                consultation_time_block=time_block,
                pdl_profile=pdl,
                location=location,
                physician=physician,
                reason=reason,
                status='scheduled',
                is_an_emergency=is_an_emergency,
                notes=notes
            )

            messages.success(request, 'Consultation scheduled successfully.')
            return redirect('consultations:consultation_calendar')

        except Exception as e:
            messages.error(request, f'Error scheduling consultation: {str(e)}')
            return redirect('consultations:create_consultation')

    return render(request, 'consultations/create_consultation.html')
    
def pdl_list_api(request):
    pdls = PDLProfile.objects.all()
    formatted_pdls = [
        {
            'id': pdl.id,
            'name': f"{pdl.username.first_name} {pdl.username.last_name}",
            'email': pdl.username.email,
        }
        for pdl in pdls
    ]
    return JsonResponse(formatted_pdls, safe=False)


def physician_list_api(request):
    physicians = Physician.objects.all()
    formatted_physicians = [
        {
            'id': physician.id,
            'name': f"{physician.username.first_name} {physician.username.last_name}",
            'email': physician.username.email,
        }
        for physician in physicians
    ]
    return JsonResponse(formatted_physicians, safe=False)

def location_list_api(request):
    locations = ConsultationLocation.objects.all()
    formatted_locations = [
        {
            'id': location.id,
            'room_number': location.room_number
        }
        for location in locations
    ]
    return JsonResponse(formatted_locations, safe=False)

def consultation_reason_list_api(request):
    reasons = ConsultationReason.objects.all()
    formatted_reasons = [
        {
            'id': reason.id,
            'reason': reason.reason,
            'description': reason.description
        }
        for reason in reasons
    ]
    return JsonResponse(formatted_reasons, safe=False)

def consultation_time_block_list_api(request):
    time_blocks = []
    for block in ConsultationTimeBlock:
        # Only include office hours
        if "08:00" <= block.value[0] <= "17:00":
            time_blocks.append({
                'value': block.name,  # Send the enum name instead of the time
                'display': block.value[1]  # Send the formatted display time
            })
    return JsonResponse(time_blocks, safe=False)