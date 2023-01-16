from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "name", "password", "confirm_password",
                  "binance_key", "binance_secret")
        extra_kwargs = {
            'kucoin_key': {'write_only': True, 'required': True},
            'kucoin_secret': {'write_only': True, 'required': True},
        }

    def validate(self, attrs) -> dict:

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return super().validate(attrs)

    def create(self, validated_data) -> User:
        validated_data.pop('confirm_password')

        return User.objects.create_user(**validated_data)