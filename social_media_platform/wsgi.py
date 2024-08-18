"""
WSGI config for social_media_platform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_platform.settings')

application = get_wsgi_application()

# In manage.py or settings.py
import django
from django.conf import settings

print(settings.INSTALLED_APPS)
django.setup()
