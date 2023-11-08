#!/bin/sh

set -e
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations superadmin
python manage.py migrate
# this for development
exec python manage.py runserver 0.0.0.0:3001
# this is for production
#gunicorn backend.wsgi:application --bind 0.0.0.0:3001
