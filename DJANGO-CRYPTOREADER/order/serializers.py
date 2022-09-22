from pyexpat import model
from .models import Order
from rest_framework.serializers import ModelSerializer


class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
