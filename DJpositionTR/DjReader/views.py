#DRF
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
#DRF-JWT
from rest_framework_simplejwt.authentication import JWTAuthentication
#My apps
from useAuthApp.models import UserForkucoin , Position
from .serializers import YourModelSerializer

numberOfTreads=7
host="127.0.0.1"
port=6379
db=0

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def activePositionTracking(request):
    username=get_username_from_token(request)
    user = User.objects.get(username=username)
    user.activePositionTracking=True
    user.save()
    return Response({'msg':"activePositionTracking activeted"})
  
def get_username_from_token(request):
    authentication = JWTAuthentication()
    try:
        user, _ = authentication.authenticate(request)  # Authenticate the request
        username = user.username  # Access the username from the authenticated user object
        return username
    except:
        # Handle authentication errors
        return None

def kucoinReader(api_key,api_secret,api_passphrase):
    totalpositions=int(callKucon(api_key,api_secret,api_passphrase)['totalNum'])
    items=[]
    currentPage=range(0,totalpositions)
    with Pool(numberOfTreads) as p:
        data=p.starmap(callKucon, zip(repeat(api_key), repeat(api_secret) , repeat(api_passphrase),repeat(endpoint),currentPage))
        items+=data['data']
    return items

def callKucon(api_key,api_secret,api_passphrase,currentPage=1):

    url = 'https://api-futures.kucoin.com/api/v1/positions?status=active&currentPage='+str(currentPage)+'&pageSize=1'
    now = int(time.time() * 1000)
    
    str_to_sign = str(now) + 'GET' + '/api/v1/positions?status=active&currentPage='+str(currentPage)+'&pageSize=1'
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    
    passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }
    
    response = requests.request('get', url, headers=headers)
    
    return response.json()

def saveToRedisAndDB(dataArry,host,port,db,userid):
    r = redis.Redis(host, port, db)
    r.set(userid,dataArry)

    for data in dataArry:
        q=Position()
        q.owner=UserForkucoin.objects.get(pk=1)
        q.id = data['id']
        q.symbol = data['symbol']
        q.autoDeposit = data['autoDeposit']
        q.maintMarginReq = data['maintMarginReq']
        q.riskLimit = data['riskLimit']
        q.realLeverage = data['realLeverage']
        q.crossMode = data['crossMode']
        q.delevPercentage = data['delevPercentage']
        q.openingTimestamp = data['openingTimestamp']
        q.currentQty = data['currentQty']
        q.currentCost = data['currentCost']
        q.currentComm = data['currentComm']
        q.unrealisedCost = data['unrealisedCost']
        q.realisedGrossCost = data['realisedGrossCost']
        q.realisedCost = data['realisedCost']
        q.isOpen = data['isOpen']
        q.markPrice = data['markPrice']
        q.markValue = data['markValue']
        q.posCost = data['posCost']
        q.posCross = data['posCross']
        q.posInit = data['posInit']
        q.posComm = data['posComm']
        q.posLoss = data['posLoss']
        q.posMargin = data['posMargin']
        q.posMaint = data['posMaint']
        q.maintMargin = data['maintMargin']
        q.realisedGrossPnl = data['realisedGrossPnl']
        q.realisedPnl = data['realisedPnl']
        q.unrealisedPnl = data['unrealisedPnl']
        q.unrealisedPnlPcnt = data['unrealisedPnlPcnt']
        q.unrealisedRoePcnt = data['realisedGrossPnl']
        q.avgEntryPrice = data['realisedPnl']
        q.liquidationPrice = data['unrealisedPnl']
        q.settleCurrency = data['unrealisedPnlPcnt']
        q.isInverse = data['realisedGrossPnl']
        q.userId = data['realisedPnl']
        q.maintainMargin = data['unrealisedPnl']
        q.save()#or update
    
def saveToRedisAndDB_paraler(dataArry,host,port,db):
    with Pool(numberOfTreads) as p:
        p.starmap(saveToRedisAndDB, zip(dataArry, repeat(host), repeat(port) , repeat(db),repeat(userid)))

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def positions(request):
    responseData=''
    username=get_username_from_token(request)
    user = User.objects.get(username=username)

    try:
        responseData = redis_client.get(user.id)
    except:
        positions = Position.objects.filter(owner=user)
        serializer = YourModelSerializer(positions, many=True)
        responseData = serializer.data
    return Response(responseData)
        