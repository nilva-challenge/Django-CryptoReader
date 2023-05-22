from DJpositionTR.celery import app
from . import views

@app.task
def trackPositions():
    users=UserForkucoin.objects.filter(activePositionTracking=True)

    for user in users:
        api_key = user.api_key
        api_secret = user.api_secret
        api_passphrase = user.api_passphrase
        positions=views.kucoinReader(views.api_key,api_secret,api_passphrase)
        views.saveToRedisAndDB_paraler(positions,views.host,views.port,views.db)
        
