from rest_framework import serializers
from kucoin.models import Order


class OrderSerializers(serializers.ModelSerializer):
    '''
        Serializer for order model with all fields
    '''

    class Meta:
        model = Order
        fields = '__all__'


class TrackSerializers(serializers.Serializer):
    '''
        track boolean field
    '''

    track = serializers.BooleanField()
