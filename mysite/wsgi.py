"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

# sys.path.append("/home/admin1/miniconda3/bin")
sys.path.append("/home/admin1/miniconda3/envs/qm2/lib/python3.5/site-packages")
# sys.path.append("./utils")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
