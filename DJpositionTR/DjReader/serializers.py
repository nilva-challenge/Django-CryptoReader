from rest_framework import serializers
from useAuthApp.models import Position


class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


