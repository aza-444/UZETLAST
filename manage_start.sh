    #!/bin/bash
set -e
cd /home/runner/workspace/website

echo "Running migrations..."
python3 manage.py migrate --run-syncdb

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Creating superuser if not exists..."
python3 manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('DJANGO_ADMIN_USER', 'admin')
password = os.environ.get('DJANGO_ADMIN_PASS', '')
email = os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@uzenergo.uz')

if not password:
    import secrets
    password = secrets.token_urlsafe(16)
    print(f'[WARN] DJANGO_ADMIN_PASS not set. Generated password: {password}')
    print('[WARN] Set DJANGO_ADMIN_PASS env var to keep a stable password.')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser created: {username}')
else:
    print(f'Superuser already exists: {username}')
"

echo "Loading initial data..."
python3 seed_data.py

echo "Starting Django server..."
exec python3 manage.py runserver 0.0.0.0:8000
