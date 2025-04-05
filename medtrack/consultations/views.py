from django.shortcuts import render
from .models import Consultation
import calendar
from datetime import date, timedelta

def consultation_calendar(request):
    """
    View function to display all consultation appointments in a calendar format.
    """
    # Get all consultations
    consultations = Consultation.objects.all()

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

    return render(request, 'consultations/consultation_calendar.html', context)
