from rest_framework import serializers

from .models import Position


class PositionSerializer(serializers.ModelSerializer):
    """
    This serializer has been customized based partial received data from following api
    https://api-futures.kucoin.com/api/v1/position?symbol={symbol_name}
    """
    class Meta:
        model = Position
        fields = ('symbol', 'created_at', 'mark_price', 'mark_value', 'risk_limit')


class TrackingPositionSerializer(serializers.ModelSerializer):
    """
    this serializer is used to filter some additional information in all positions.
    It has been applied in serializing_output method in Utility class.( it is located in tasks.py)
    """
    class Meta:
        model = Position
        fields = ('symbol', 'created_at', 'mark_price', 'mark_value', 'risk_limit')

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        return Position.objects.create(user_id=user_id, **validated_data)
