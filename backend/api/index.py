"""
Vercel Serverless Function Entry Point
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.core.wsgi import get_wsgi_application

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

def handler(req, res):
    from django.conf import settings
    from whitenoise import WhiteNoise
    
    # Add WhiteNoise for static files
    if not hasattr(application, 'whitenoise'):
        application = WhiteNoise(application, root=os.path.join(settings.BASE_DIR, 'staticfiles'))
        for directory in getattr(settings, 'STATICFILES_DIRS', []):
            application.add_files(directory)
    
    from mangum import Mangum
    asgi_handler = Mangum(application)
    return asgi_handler(req, res)
