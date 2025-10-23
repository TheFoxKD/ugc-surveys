"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    msg = """
    DJANGO_SETTINGS_MODULE is not set.
    Export it to 'src.config.settings.dev' or 'src.config.settings.prod'
    """
    raise RuntimeError(msg)

application = get_wsgi_application()
