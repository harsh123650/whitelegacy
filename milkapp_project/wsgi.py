import os
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for the 'wsgi' command-line environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'milkapp_project.settings')

# Get the WSGI application object for use by any WSGI server
application = get_wsgi_application()
