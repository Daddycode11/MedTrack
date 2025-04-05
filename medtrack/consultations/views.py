from django.shortcuts import render, redirect, get_object_or_404
from .models import Consultation, Physician
import calendar
from datetime import date, timedelta
from django.contrib import messages
from .forms import ScheduleConsultationForm

def consultation_calendar(request, consultations):#
    """
    View function to display all consultation appointments in a calendar format.
    """
    # Get all consultations
   
    # Prepare data for the calendar
    today = date.today()
    year = request.GET.get('year', today.year)
    month = request.GET.get('month', today.month)
    year, month = int(year), int(month)

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
    View function to display all consultations.
    """
    # Fetch all consultations
    consultations = Consultation.objects.all()

    # Get the calendar data
    context = consultation_calendar(request, consultations)

    # Render the template
    return render(request, "consultations/consultation_calendar.html", context)

def consultations_by_physician(request, physician_id):
    """
    View function to display consultations for a specific physician.
    """
    physician = get_object_or_404(Physician, id=physician_id)
    # Fetch consultations for the specified physician
    consultations = Consultation.objects.filter(physician=physician)

    # Get the calendar data
    context = consultation_calendar(request, consultations)

    # Render the template
    return render(request, "consultations/consultation_calendar.html", context)
from datetime import date
from django.shortcuts import render, get_object_or_404
from .models import Physician, Consultation

def doctor_dashboard(request):
    """
    View function to display the doctor's dashboard.
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
    View to schedule a new consultation.
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
    View to cancel a consultation with confirmation.
    """
    consultation = get_object_or_404(Consultation, id=consultation_id)

    if request.method == 'POST':
        # Mark the consultation as canceled
        consultation.status = 'canceled'
        consultation.save()

        # Add a success message
        messages.success(request, f"Consultation with {consultation.physician} on {consultation.consultation_date_date_only} has been canceled.")
        return redirect('consultations:consultation_calendar')

    return render(request, 'consultations/cancel_consultation.html', {'consultation': consultation})