from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(
        required=True, write_only=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message='a user is already registered with this username!')]
        )
    api_key = serializers.CharField(required=True, write_only=True)
    secret_key = serializers.CharField(required=True, write_only=True)
    api_passphrase = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})
    
    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})

    def validate(self, attrs):
        return super().validate(attrs)

