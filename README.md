# medtrack-django
Medtrack Django Capstone project

# Installation

1. Clone the repository. You must have git installed on your machine. On GitHub, click the green "Code" button and copy the URL in the tab "HTTPS". Then, in your terminal, run:
```bash
git clone <URL>
```

2. Navigate to the project directory:
```bash
cd medtrack-django
```

3. Create a virtual environment:
```bash
python3 -m venv env
```
4. Activate the virtual environment:
```bash
# On Windows
.\env\Scripts\activate
# On MacOS/Linux
source env/bin/activate
```
5. Install the required packages:
```bash
pip install -r requirements.txt
```

6. Once the packages are installed, you can run the server:
```bash
cd medtrack
python manage.py runserver
```

# Initialization

1. Run the following command to create the database and apply migrations:
```bash
cd medtrack
# Create the database
python manage.py makemigrations
python manage.py migrate
```

2. Create a superuser to access the admin panel:
```bash
python manage.py createsuperuser
```

3. Run the `initialize` command to create the initial data for the lookup tables:
```bash
python manage.py initialize
```

# Recommendations

The following recommendations from the panel review have been implemented in this system:

| # | Recommendation | Status |
|---|----------------|--------|
| 2 | Input 100–200 PDL data — generate realistic Filipino PDL profiles with assigned health conditions for testing and demonstration purposes | Done |
| 3 | Simulation of the workflow process — schedule initial consultation, dispense medication for 7 days, schedule a follow-up consultation after 7 days for clearance/certification, and record findings after medication | Done |
| 4 | Report generation — produce consultation summary reports with statistics and filters | Done |
| 5 | Monitoring of transactions and PDLs with chronic conditions (hypertension, diabetes, heart problem) — track which PDLs have these conditions and their consultation history | Done |
| 6 | Fast-moving medications — identify which medications are most frequently prescribed and dispensed in the facility | Done |
| 7 | Past history regarding health monitoring issues — record and view each PDL's past medical history, previous diagnoses, and ongoing health conditions | Done |
| 8 | Generate reports — produce summary reports on consultations, health conditions, medication usage, and inventory with CSV export | Done |
| 9 | User roles (admin, staff, doctor, pharmacist) — enforce role-based access control so each role can only access their permitted actions | Done |
| 11 | Deployment readiness — settings use environment variables (SECRET_KEY, DEBUG, ALLOWED_HOSTS) via python-decouple; .env.example provided | Done |
| 13 | Monitoring of medicine — track medication usage, dispensing history, and inventory levels per PDL | Done |
| 14 | Reports of medicine inventory — generate inventory reports showing stock levels, fast-moving medications, and dispensing summaries with CSV export | Done |