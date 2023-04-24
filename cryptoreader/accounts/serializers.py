from rest_framework import serializers
from .models import User, KucoinAccount
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "key",
            "secret",
            "passphrase",
        ]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class KucoinAccountSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = KucoinAccount
        exclude = ["pk_uuid"]

    def validate(self, attrs):
        return super().validate(attrs)
