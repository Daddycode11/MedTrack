# MedTrack — Health Monitoring System for PDL

A Django-based health monitoring and records management system for Persons Deprived of Liberty (PDL) at the San Jose District Jail (BJMP), Occidental Mindoro. MedTrack digitalizes consultation scheduling, prescription management, inventory tracking, and generates reports for the jail medical team.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [User Roles](#user-roles)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Initialization](#initialization)
- [Demo Data](#demo-data)
- [Environment Variables](#environment-variables)
- [Management Commands](#management-commands)
- [Panel Review Recommendations](#panel-review-recommendations)

---

## Features

### PDL Management
- Register and manage PDL profiles (demographics, civil status, educational attainment, place of birth)
- Track detention instances — room number, term length, detention status, start/end dates, reason for detention
- Add, edit, and remove PDL records atomically (User + Profile + Detention in a single transaction)
- Per-PDL health condition records (Hypertension, Diabetes, Heart Disease, Asthma, TB, Mental Health, Renal, Cancer, and others)
- View full PDL profile with active consultations, prescriptions, and health history on one page
- Filter and paginate PDL directory by name, status, and detention details

### Consultation Scheduling
- Schedule consultations with a physician, location, date, and 30-minute time block (08:00–17:00)
- Doctor dashboard showing each physician's upcoming consultations
- Monthly calendar view of all consultations across the facility
- Prevent double-booking via unique constraints: same PDL, same physician, or same room cannot have two consultations at the same time
- Mark consultations as **Completed**, **Canceled**, or **Rescheduled**
- Complete consultation form captures:
  - **Physical exam on arrival** — temperature, blood pressure, heart rate, respiratory rate, height, weight, BMI
  - **Past Medical History (PMH)** — pediatric history, major illnesses, surgeries, injuries, medication history, blood type, allergies, psychiatric history, alcohol/smoking/drug use, ARV treatment, vaccination records
  - **TB entry screening checklist** — cough, BMI, sputum, chest X-ray, prior TB treatment, exposure
  - **Final remarks** — conclusion, impressions, recommendations
- Printable consultation report for physical records

### Prescription & Medications
- Create prescriptions tied to a PDL and a physician
- Record dosage, frequency, duration, prescribed quantity, and dispensed quantity
- Prescription status auto-updates to **Dispensed** once dispensed quantity meets prescribed quantity
- Auto-deducts from medication inventory when dispensed quantity is updated
- Assign a pharmacist to each dispensing event with timestamp
- Printable prescription label
- View remaining quantity and full dispensing history per prescription

### Medication Inventory
- Maintain a medication catalog with generic name, dosage form, strength, route of administration, and manufacturer
- Track real-time inventory levels, reorder level threshold, expiration date, and storage location
- **Low-stock alerts** when quantity falls below reorder level
- **Expiration warnings** for medications nearing or past expiration date
- Full audit trail via inventory transactions: addition, dispensation, adjustment, return, expired
- Update inventory with a logged reason and automatic transaction record

### Reports & Analytics
- **Consultation Statistics** — weekly, monthly, and yearly totals with completed / scheduled / canceled / emergency breakdown; drill down into a specific period
- **Health Conditions Report** — prevalence by condition type, list of PDLs with multiple chronic conditions
- **Fast-Moving Medications** — top prescribed and dispensed medications ranked by usage count
- **Inventory Report** — current stock levels, low-stock alerts, expiration warnings, reorder recommendations
- **CSV export** available on all major reports

### User & Access Management (IT Admin Panel)
- Custom admin panel separate from the Django default `/admin/`
- Create user accounts with roles: Admin, Doctor/Nurse
- View per-user activity history: consultations conducted, prescriptions written, prescriptions dispensed, inventory transactions, health conditions recorded
- Assign or change roles inline
- Delete accounts (cannot delete own account)
- Role badge displayed in the navigation bar for every logged-in user

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 5.0.2 |
| Language | Python 3.9+ |
| Database | SQLite (dev) / PostgreSQL (production) |
| Frontend | Bootstrap 5.3 |
| Typography | DM Sans |
| Theme | Dark mode default, light mode toggle |
| Forms | django-widget-tweaks |
| Filtering | django-filter |
| Env vars | python-decouple |
| Timezone | Asia/Shanghai |

---

## User Roles

| Role | What they can do |
|---|---|
| **Admin** | Full access to all features — PDL management, consultations, prescriptions, inventory, reports, user administration |
| **Staff** | Add, edit, and delete PDL records; record health conditions; view consultations and reports |
| **Doctor / Nurse** | Schedule, complete, cancel, and reschedule consultations; write prescriptions; record health conditions; view reports |
| **Pharmacist** | Add medications, update inventory, dispense prescriptions; view reports |

All roles can view PDL profiles, consultations, prescriptions, and the report center. Access is enforced at the view level via the `@role_required` decorator. New user accounts are automatically assigned the **Staff** role by default.

---

## Installation

### Prerequisites
- Python 3.9 or higher
- Git

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/Daddycode11/MedTrack.git
cd MedTrack
```

**2. Create and activate a virtual environment**
```bash
# Create
python -m venv env

# Activate — Windows
.\env\Scripts\activate

# Activate — macOS / Linux
source env/bin/activate
```

**3. Install dependencies**
```bash
pip install -r medtrack/requirements.txt
```

**4. Start the development server**
```bash
cd medtrack
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

---

## Initialization

Run these commands once after cloning to set up the database and seed the required lookup tables.

```bash
cd medtrack

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser account
python manage.py createsuperuser

# Seed lookup data (physicians, locations, medications, reasons, specialties)
python manage.py initialize
```

---

## Demo Data

Two management commands are available for generating realistic test data.

### Generate PDL Profiles
Creates realistic Filipino PDL profiles with demographics, detention records, and health conditions.

```bash
# Generate 150 PDLs (default)
python manage.py generate_pdl_data

# Generate a specific count
python manage.py generate_pdl_data --count 200

# Clear previously generated data first, then regenerate
python manage.py generate_pdl_data --count 150 --clear
```

Generated usernames are prefixed with `pdl_gen_`.

### Simulate the Clinical Workflow
For each PDL, simulates the complete 7-day cycle:
1. **Initial consultation** (completed) — physical exam, PMH, TB screening, final remarks
2. **7-day prescription** (dispensed) — condition-appropriate medication, auto-deducts inventory
3. **Follow-up consultation** — completed with treatment findings if scheduled in the past, otherwise marked as scheduled

```bash
# Simulate 80 PDLs (default)
python manage.py simulate_workflow

# Simulate a specific count
python manage.py simulate_workflow --count 100

# Clear all simulated records first, then re-run
python manage.py simulate_workflow --count 100 --clear
```

Simulated records are tagged with `[SIM]` in notes. The command skips PDLs that have already been simulated.

**Condition → Medication mapping used during simulation:**

| Condition | Medication |
|---|---|
| Hypertension | Amlodipine |
| Diabetes | Simvastatin |
| Heart Disease | Clopidogrel |
| Asthma | Montelukast |
| Tuberculosis | Amoxil |
| Mental Health | Sertraline |

---

## Environment Variables

Copy `.env.example` to `.env` and fill in values before deploying to production.

```bash
cp medtrack/.env.example medtrack/.env
```

**.env.example**
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

| Variable | Description | Default (dev) |
|---|---|---|
| `SECRET_KEY` | Django secret key | Insecure fallback (change in production) |
| `DEBUG` | Enable debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames | Empty (all hosts allowed in dev) |

> **Production note:** Always set `DEBUG=False` and a strong `SECRET_KEY` before deploying. Consider switching from SQLite to PostgreSQL for production workloads.

---

## Management Commands

| Command | Description |
|---|---|
| `initialize` | Seed all lookup tables (physicians, locations, medications, reasons, specialties) |
| `generate_pdl_data` | Generate realistic Filipino PDL profiles with health conditions |
| `simulate_workflow` | Simulate full 7-day consultation → prescription → follow-up cycle for PDLs |
| `cleanup` | Remove test and simulation data from the database |

---

## Panel Review Recommendations

All recommendations from the capstone panel review have been implemented:

| # | Recommendation | Status |
|---|---|---|
| 2 | Input 100–200 PDL data — generate realistic Filipino PDL profiles with assigned health conditions for testing and demonstration | Done |
| 3 | Simulation of the workflow process — schedule initial consultation, dispense medication for 7 days, schedule a follow-up after 7 days for clearance/certification, and record findings after medication | Done |
| 4 | Report generation — produce consultation summary reports with statistics and filters | Done |
| 5 | Monitoring of transactions and PDLs with chronic conditions (hypertension, diabetes, heart problem) — track which PDLs have these conditions and their consultation history | Done |
| 6 | Fast-moving medications — identify which medications are most frequently prescribed and dispensed in the facility | Done |
| 7 | Past history regarding health monitoring issues — record and view each PDL's past medical history, previous diagnoses, and ongoing health conditions | Done |
| 8 | Generate reports — produce summary reports on consultations, health conditions, medication usage, and inventory with CSV export | Done |
| 9 | User roles (admin, staff, doctor, pharmacist) — enforce role-based access control so each role can only access their permitted actions | Done |
| 11 | Deployment readiness — settings use environment variables (SECRET_KEY, DEBUG, ALLOWED_HOSTS) via python-decouple; .env.example provided | Done |
| 13 | Monitoring of medicine — track medication usage, dispensing history, and inventory levels per PDL | Done |
| 14 | Reports of medicine inventory — generate inventory reports showing stock levels, fast-moving medications, and dispensing summaries with CSV export | Done |
