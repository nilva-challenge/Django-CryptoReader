from rest_framework import serializers

class PositionTrackingSerializer(serializers.Serializer):
    track = serializers.BooleanField(required=True, write_only=True)

    def validate(self, attrs):
        return super().validate(attrs)