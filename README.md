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