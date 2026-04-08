#!/bin/bash
set -e

echo "Waiting for database to be ready..."
while ! python -c "import pymysql; pymysql.connect(host='db', user='order_user', password='order_pass', database='order_management')" 2>/dev/null; do
  echo "Database is unavailable - sleeping"
  sleep 1
done

echo "Database is ready!"

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Creating admin user if not exists..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Admin user created: admin / admin123')
else:
    print('Admin user already exists')
EOF

echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000
