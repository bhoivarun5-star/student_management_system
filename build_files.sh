#!/bin/bash
# Build script for Vercel — runs during deployment

set -e  # Exit on any error

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
cd student_system
python manage.py collectstatic --noinput

echo "==> Build complete!"
