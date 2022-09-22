
from rest_framework.viewsets import ModelViewSet
from .serializers import OrderSerializer


class CampaignViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    
