#!/bin/sh

set -e
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations superadmin
python manage.py migrate
exec python manage.py runserver 0.0.0.0:3001
