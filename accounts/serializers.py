from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "name", "password", "confirm_password",
                  "api_future_key", "api_future_secret", "api_spot_key", "api_spot_secret")
        extra_kwargs = {
            'api_future_key': {'write_only': True, 'required': True},
            'api_future_secret': {'write_only': True, 'required': True},
            'api_spot_key': {'write_only': True, 'required': True},
            'api_spot_secret': {'write_only': True, 'required': True},
        }

    def validate(self, data) -> dict:
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        if data['api_future_secret'] is not None and data['api_future_key'] is None:
            raise serializers.ValidationError({"empty field": "You can't fill the api_future_secret but put empty the "
                                                              "api_future_secret "})
        if data['api_future_secret'] is None and data['api_future_key'] is not None:
            raise serializers.ValidationError({"empty field": "You can't fill the api_future_secret but put empty the "
                                                              "api_future_key"})
        if data['api_spot_secret'] is not None and data['api_spot_key'] is None:
            raise serializers.ValidationError({"empty field": "You can't fill the api_spot_secret but put empty the "
                                                              "api_spot_secret "})
        if data['api_spot_secret'] is None and data['api_spot_key'] is not None:
            raise serializers.ValidationError({"empty field": "You can't fill the api_spot_secret but put empty the "
                                                              "api_spot_key"})

        return super().validate(data)

    def create(self, validated_data) -> User:
        validated_data.pop('confirm_password')

        return User.objects.create_user(**validated_data)
