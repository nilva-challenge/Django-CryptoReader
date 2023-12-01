from rest_framework import serializers
from .models import Order


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class SymbolTrackSerializers(serializers.Serializer):
    track = serializers.CharField(required=True, max_length=64)
