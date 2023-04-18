from rest_framework import serializers

from .models import Position


class PositionSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField()
    #
    # class Meta:
    #     model = Position
    #     fields = '__all__'
    #     # exclude = ('user',)
    #     read_only_fields = ('symbol', 'created_at', 'mark_price', 'mark_value', 'rist_limit')
    class Meta:
        model = Position
        fields = ('symbol', 'created_at', 'mark_price', 'mark_value', 'risk_limit')

class TrackingPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = ('symbol', 'created_at', 'mark_price', 'mark_value', 'risk_limit')

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        return Position.objects.create(user_id=user_id, **validated_data)
