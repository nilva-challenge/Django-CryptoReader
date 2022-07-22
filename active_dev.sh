set -o allexport
. ./config/gunicorn.dev.env
. ./config/django.dev.env
. ./config/postgres.dev.env
set +o allexport