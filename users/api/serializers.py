from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from utils.encryption import encrypt, decrypt

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'api_key',
            'api_secret',
            'api_passphrase',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }
    
    def create(self, validated_data):
        """
            Hash password and encrypt api details for safety.
        """
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['api_key'] = encrypt(validated_data['api_key'])
        validated_data['api_secret'] = encrypt(validated_data['api_secret'])
        validated_data['api_passphrase'] = encrypt(validated_data['api_passphrase'])
        return User.objects.create(**validated_data)

    def to_representation(self, instance):
        """
            Decrypt api details to show to user.
        """
        ret = super().to_representation(instance)
        ret['api_key'] = decrypt(ret['api_key'])
        ret['api_secret'] = decrypt(ret['api_secret'])
        ret['api_passphrase'] = decrypt(ret['api_passphrase'])
        return ret
