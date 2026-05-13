#!/usr/bin/env python
"""
Run via cPanel Python App → Execute python script:
    /home/bejundas/bejundas-platform/scripts/create_admin.py

Creates the initial superuser. Change the password immediately after first login.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

import django  # noqa: E402

django.setup()

from django.contrib.auth import get_user_model  # noqa: E402

User = get_user_model()

USERNAME = "admin"
EMAIL = "info@bejundas.co.tz"
PASSWORD = "Bejundas@2026!"

if User.objects.filter(username=USERNAME).exists():
    print(f"Superuser '{USERNAME}' already exists — no changes made.")
else:
    User.objects.create_superuser(username=USERNAME, email=EMAIL, password=PASSWORD)
    print("Superuser created successfully.")
    print(f"  Username : {USERNAME}")
    print(f"  Password : {PASSWORD}")
    print("IMPORTANT: Change this password immediately after your first login.")
