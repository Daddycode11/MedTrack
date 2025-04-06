# 03. Consultations Application

## Table of Contents
1. [SQL Data Model](#sql-data-model)
    - [MedicalSpecialty](#medicalspecialty)
    - [Physician](#physician)
    - [ConsultationLocation](#consultationlocation)
    - [ConsultationReason](#consultationreason)
    - [ConsultationTimeBlock](#consultationtimeblock)
    - [Consultation](#consultation)
2. [Views, URLs, and Forms](#views-urls-and-forms)
    - [consultation_calendar](#consultation_calendar)
    - [all_consultations](#all_consultations)
    - [consultations_by_physician](#consultations_by_physician)
    - [doctor_dashboard](#doctor_dashboard)
    - [schedule_consultation](#schedule_consultation)
    - [cancel_consultation](#cancel_consultation)
    - [reschedule_consultation](#reschedule_consultation)
3. [Consultations App URL Configuration](#consultations-app-url-configuration)
    - [Routes](#routes)
    - [Namespace](#namespace)
    - [URL Patterns](#url-patterns)

## SQL Data Model

![Consultations Schema](img/schema_consultations.png)

### `MedicalSpecialty`

Represents a medical specialty.

- **Fields**:
  - `name (CharField)`: The name of the medical specialty (max length: 100).
  - `description (TextField)`: A description of the medical specialty.

- **Meta Options**:
  - `verbose_name`: "Medical Specialty".
  - `verbose_name_plural`: "Medical Specialties".
  - `ordering`: Ordered by `name`.

- **Methods**:
  - `__str__`: Returns the name of the medical specialty.

---

### `Physician`

Represents a doctor.

- **Fields**:
  - `username (ForeignKey)`: A reference to the `User` model.
  - `employee_type (CharField)`: The type of employment (choices: `full_time`, `part_time`, `contract`).
  - `specialty (ForeignKey)`: A reference to the `MedicalSpecialty` model.
  - `phone_number (CharField)`: The physician's phone number (max length: 15).
  - `address (CharField)`: The physician's address (max length: 255).

- **Meta Options**:
  - `verbose_name`: "Physician".
  - `verbose_name_plural`: "Physicians".
  - `ordering`: Ordered by the physician's last name.

- **Methods**:
  - `__str__`: Returns the physician's full name and specialty.

---

### `ConsultationLocation`

Represents a consultation location.

- **Fields**:
  - `room_number (CharField)`: The room number (max length: 10).
  - `capacity (IntegerField)`: The capacity of the room.

- **Meta Options**:
  - `verbose_name`: "Consultation Location".
  - `verbose_name_plural`: "Consultation Locations".
  - `ordering`: Ordered by `room_number`.

- **Methods**:
  - `__str__`: Returns the room number.

---

### `ConsultationReason`

Represents a reason for consultation.

- **Fields**:
  - `reason (CharField)`: The reason for the consultation (max length: 255).
  - `description (TextField)`: A description of the reason (optional).

- **Meta Options**:
  - `verbose_name`: "Consultation Reason".
  - `verbose_name_plural`: "Consultation Reasons".
  - `ordering`: Ordered by `reason`.

- **Methods**:
  - `__str__`: Returns the reason.

---

### `ConsultationTimeBlock`

An enumeration representing 30-minute time blocks for consultations.

- **Values**:
  - `BLOCK_01` to `BLOCK_48`: Representing time blocks from `00:00` to `23:30`.

---

### `Consultation`

Represents a consultation.

- **Fields**:
  - `pdl_profile (ForeignKey)`: A reference to the `PDLProfile` model.
  - `physician (ForeignKey)`: A reference to the `Physician` model.
  - `location (ForeignKey)`: A reference to the `ConsultationLocation` model.
  - `reason (ForeignKey)`: A reference to the `ConsultationReason` model.
  - `status (CharField)`: The status of the consultation (choices: `scheduled`, `completed`, `canceled`).
  - `consultation_date_date_only (DateField)`: The date of the consultation.
  - `consultation_time_block (CharField)`: The time block of the consultation (choices: `ConsultationTimeBlock`).
  - `is_an_emergency (BooleanField)`: Indicates if the consultation is an emergency.
  - `notes (TextField)`: Additional notes for the consultation (optional).

- **Meta Options**:
  - `verbose_name`: "Consultation".
  - `verbose_name_plural`: "Consultations".
  - `ordering`: Ordered by `consultation_date_date_only` and `consultation_time_block`.
  - **Constraints**:
     - Unique consultation per PDL profile, date, and time block.
     - Unique consultation per physician, date, and time block.
     - Unique consultation per location, date, and time block.

- **Methods**:
  - `__str__`: Returns a string representation of the consultation, including the physician, date, time block, and location.
  - `consultation_time_block_display`: Returns the display value of the consultation time block.

## Views, URLs, and Forms

### `consultation_calendar`

Generates a calendar view for consultations within a specified month and year.

**Args**:
- `request (HttpRequest)`: The HTTP request object containing optional `year` and `month` query parameters to specify the calendar's year and month. Defaults to the current year and month if not provided.
- `consultations (QuerySet)`: A queryset of consultation objects, each containing a `consultation_date_date_only` attribute representing the date of the consultation.

**Returns**:
- `dict`: A context dictionary containing:
  - `calendar_data (list)`: A list of weeks, where each week is a list of dictionaries representing days.
  - `year (int)`: The year of the calendar.
  - `month (int)`: The month of the calendar.
  - `month_name (str)`: The full name of the month.
  - `prev_month (int)`: The previous month (1-12).
  - `prev_year (int)`: The year corresponding to the previous month.
  - `next_month (int)`: The next month (1-12).
  - `next_year (int)`: The year corresponding to the next month.

---

### `all_consultations`

Handles the retrieval and display of all consultations.

**Args**:
- `request (HttpRequest)`: The HTTP request object.

**Returns**:
- `HttpResponse`: The rendered consultation calendar template with the context containing consultation data.

---

### `consultations_by_physician`

Handles the retrieval and display of consultations for a specific physician.

**Args**:
- `request (HttpRequest)`: The HTTP request object.
- `physician_id (int)`: The ID of the physician whose consultations are to be retrieved.

**Returns**:
- `HttpResponse`: A rendered HTML page displaying the consultation calendar for the specified physician.

**Raises**:
- `Http404`: If no `Physician` object with the given ID is found.

---

### `doctor_dashboard`

Displays the doctor's dashboard with relevant information.

**Args**:
- `request (HttpRequest)`: The HTTP request object.

**Returns**:
- `HttpResponse`: The rendered HTML template for the doctor's dashboard.

**Context**:
- `physician (Physician)`: The physician object for 'jessicaadams'.
- `upcoming_consultations (QuerySet)`: A queryset containing up to three upcoming consultations for the physician, sorted by date and time.

---

### `schedule_consultation`

Handles the scheduling of a consultation.

**Args**:
- `request (HttpRequest)`: The HTTP request object containing metadata about the request.

**Returns**:
- `HttpResponse`: Renders the consultation scheduling page with the form for GET requests or redirects to the consultation calendar for valid POST requests.

---

### `cancel_consultation`

Handles the cancellation of a consultation.

**Args**:
- `request (HttpRequest)`: The HTTP request object.
- `consultation_id (int)`: The ID of the consultation to be canceled.

**Returns**:
- `HttpResponse`: Renders the cancellation confirmation page if the request method is not POST. Redirects to the consultation calendar if the consultation is successfully canceled.

---

### `reschedule_consultation`

Handles the rescheduling of a consultation.

**Args**:
- `request (HttpRequest)`: The HTTP request object containing metadata about the request.
- `consultation_id (int)`: The ID of the consultation to be rescheduled.

**Returns**:
- `HttpResponse`: Renders the reschedule consultation page with the form if the request is not a POST, or redirects to the consultation calendar upon successful form submission.

**Raises**:
- `Http404`: If the consultation with the given ID does not exist.

**Template**:
- `consultations/reschedule_consultation.html`

**Context**:
- `form (ScheduleConsultationForm)`: The form for scheduling the consultation.
- `consultation (Consultation)`: The consultation object being rescheduled.

## Consultations App URL Configuration

This module defines the URL patterns for the `consultations` app, mapping specific URL paths to their corresponding view functions. These URLs handle various functionalities such as viewing the doctor dashboard, managing consultation schedules, and handling consultation cancellations and rescheduling.

### Routes

- **`doctor-dashboard`**: Displays the doctor's dashboard.
- **`calendar/`**: Displays all consultations in a calendar view.
- **`calendar-physician/<int:physician_id>/`**: Displays consultations filtered by a specific physician.
- **`schedule/`**: Allows scheduling a new consultation.
- **`cancel/<int:consultation_id>/`**: Cancels a specific consultation.
- **`reschedule/<int:consultation_id>/`**: Reschedules a specific consultation.

### Namespace

- **`app_name`**: `'consultations'` (used for namespacing URLs in templates and reverse lookups).

### URL Patterns

```python
from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
     path('doctor-dashboard', views.doctor_dashboard, name='doctor_dashboard'),
     path('calendar/', views.all_consultations, name='consultation_calendar'),
     path('calendar-physician/<int:physician_id>/', views.consultations_by_physician, name='consultation_calendar_physician'),
     path('schedule/', views.schedule_consultation, name='schedule_consultation'),
     path('cancel/<int:consultation_id>/', views.cancel_consultation, name='cancel_consultation'),
     path('reschedule/<int:consultation_id>/', views.reschedule_consultation, name='reschedule_consultation'),
     # Other URLs...
]
```