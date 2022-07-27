#!/bin/sh

python manage.py makemigrations --noinput && python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py superuser && mkdir -p supervisor && supervisord -c supervisord.conf














