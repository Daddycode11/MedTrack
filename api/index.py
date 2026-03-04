import sys
import os

# Add the Django project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'medtrack'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medtrack.settings')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
