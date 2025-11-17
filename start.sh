#!/usr/bin/env bash
set -euo pipefail

echo "Attendo il database..."
while ! python -c "import psycopg; psycopg.connect('dbname=${POSTGRES_DB} user=${POSTGRES_USER} password=${POSTGRES_PASSWORD} host=${POSTGRES_HOST}')"; do
  sleep 1
done

echo "Database pronto, applico le migrazioni..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Import dei CSV..."
export PYTHONPATH=/app
python /app/data_import/import_script.py

echo "Avvio server..."
python manage.py runserver 0.0.0.0:8000