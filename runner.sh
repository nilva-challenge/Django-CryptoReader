echo "Makemigrations and migrate..."
python3 manage.py makemigrations --noinput 
python3 manage.py migrate --noinput 

echo "Collectstatic..."
python3 manage.py collectstatic --noinput 

echo "Start celery worker..."
celery -A crypto_reader worker --beat --scheduler django --loglevel=info &

echo "Runserver"
python3 manage.py runserver
