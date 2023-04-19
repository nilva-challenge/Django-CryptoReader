# In name of Allah

## Introduction
We want to develop a REST based django application to read signed in user's KuCoin open positions for them. For this to happen, you must be able to read user's positions (if requested from user) every 30 seconds. 

The application you develop must have these features:
- Users should be able to **sign up** (provide name, username & kucoin details).
- Users should be able to **sign in**.
- Users should be able to **request position tracking**.
- Users should be able to **see list** of current open positions.
- Current positions must be cached. **The cache should be in redis and must have a fallback to database if redis was down.**
- Application should be able to track user's positions every 30 seconds.
- Application should be able to handle multi users.
- Application must be able to resume its job after restart.

You can use [this api](https://docs.kucoin.com/#list-accounts) from KuCoin to handle this. You should create KuCoin account if you do not have already & get api key & secret to test your implementation. Note we do not need your api key, that is only for your own usage.

### Note
- We do **NOT want any kind of UI** from you 
- KuCoin api key & secrets should not be stored in raw format
 
 
## Expectations:
We want a clean, readable and maintainable code with meaningful comments and docstrings. Also you need to provide postman API doc for web app. 

## Task
1. Fork this repository
2. Develop the challenge with Django 3 or higher
3. Push your code to your repository
4. Send us a pull request, we will review and get back to you
5. Enjoy 

#----------------------------------------------------------------
# All functions which have been performed in the system 
- User is able to sign up , sign in, request to track position(per symbol)
- Authentication has been implemented (JWT token)
- User is able to see list of positions (cache system is applied)
- KuCoin api key & secrets are stored in encrypted format
- The system can handle multiuser requests for tracking
- Swagger has been provided in `/docs` endpoint
- pagination is provided in `/positions` endpoint
- All endpoints must be set **access token** in head as **Authorization** with prefix JWT except for `auth/user`
## All dependencies
- Redis has been applied as message broker and cache system
- Celery has been applied as  task queue
- MySQL or Sqlite has been applied as database (default database is `MySQL`)
## Installation
- activate virtualenv
- install all python requirments by `pip install -r requirements.txt`
- migrate database through `python manage.py migrate`
-  **check the following fields** in settings.py
1) `CELERY_BROKER_URL`
2) `CELERY_RESULT_BACKEND`
3) `CELERY_TASK_SERIALIZER`
4) `CELERY_RESULT_SERIALIZER`
5) `CELERY_ACCEPT_CONTENT`
6) `CELERY_BEAT_SCHEDULER ,CACHES ,EXPIRE_TIME`
7) `TARGET_SCHEDULE_APP_NAME, INTERVAL`

- Change the database backend in setting.py
- Ensure that the database and redis are installed and available.
- Run these commands in separate shells in the same python virtualenv.
1) `celery -A position beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`
2) `celery -A position worker -l info -P gevent`
3) in development mode (`python manage.py runserver`), but you are able to use gunicorne or uwsgi
## Admin Panel
- If you register as superuser can access the `PERIODIC TASK`, it allows you to enable or disable every task whatever you want.
