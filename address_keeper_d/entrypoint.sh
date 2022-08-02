#!/bin/bash

python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py createsuperuser --no-input

gunicorn address_keeper.wsgi:application --bind 0.0.0.0:8000