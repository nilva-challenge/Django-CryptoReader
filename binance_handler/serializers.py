from abc import ABC

from rest_framework import serializers
from .models import Order, Position, Binance_profile


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class PositionSerializers(serializers.ModelSerializer):
    class Meta:
        model: Position
        fields = '__all__'


class TrackSerializers(serializers.Serializer):
    track = serializers.BooleanField()


class BinanceProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model: Binance_profile
        fields = '__all__'
