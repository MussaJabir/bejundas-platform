import os
import sys

import environ

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

sys.path.insert(0, BASE_DIR)

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
