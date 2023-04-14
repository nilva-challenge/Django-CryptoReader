#!/bin/bash

echo "Create and activated venv..."
pip install virtualenv
python3 -m virtualenv venv
if [ "$OSTYPE" == "linux-gnu" ]; then
source venv/bin/activate
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
.\venv\Scripts\activate.bat
fi
pip install --upgrade pip
pip install -r requirements.txt

echo "Makemigrations and migrate..."
python3 manage.py makemigrations --noinput 
python3 manage.py migrate --noinput 

echo "Collectstatic..."
python3 manage.py collectstatic --noinput 

echo "Start celery worker in background..."
celery -A crypto_reader worker --beat --scheduler django --loglevel=info &

echo "Runserver"
python3 manage.py runserver
