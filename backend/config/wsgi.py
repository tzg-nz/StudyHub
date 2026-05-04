import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application

from dotenv import load_dotenv
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
