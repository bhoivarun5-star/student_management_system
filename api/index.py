import os
import sys
from pathlib import Path

# ── Add the Django project directory to Python path ──────────────────────────
# Project layout:
#   /api/index.py          ← this file (Vercel entry point)
#   /student_system/       ← Django project root (contains manage.py)
#   /student_system/student_system/settings.py

project_root = Path(__file__).resolve().parent.parent          # repo root
django_dir   = project_root / 'student_system'                 # where manage.py lives

sys.path.insert(0, str(django_dir))

# ── Point Django to our settings module ──────────────────────────────────────
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_system.settings')

# ── Bootstrap Django & export the WSGI app ───────────────────────────────────
from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()   # Vercel looks for a variable named 'app'
