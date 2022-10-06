from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    '''
        User serializers for register
    '''

    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "name", "password", "confirm_password",
                  "kucoin_key", "kucoin_secret", "kucoin_passphrase")
        extra_kwargs = {
            'kucoin_key': {'write_only': True, 'required': True},
            'kucoin_secret': {'write_only': True, 'required': True},
            'kucoin_passphrase': {'write_only': True, 'required': True},
        }

    def validate(self, attrs) -> dict:
        '''
        Checking password & other fields
        '''

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return super().validate(attrs)

    def create(self, validated_data) -> User:
        validated_data.pop('confirm_password')

        return User.objects.create_user(**validated_data)
