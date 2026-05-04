import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

os.environ['VERCEL'] = '1'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
