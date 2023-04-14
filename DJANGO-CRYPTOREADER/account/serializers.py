from .utils.utility import encrypt_message, decrypt_message
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from .utils.utility import encrypt_message, decrypt_message
from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'kucoin_api_secret',
                  'kucoin_api_key', 'kucoin_pass_pharese')

    def create(self, validated_data):
        user = super().create({
            'username': self.validated_data['username'],
            'kucoin_api_secret': encrypt_message(str(self.validated_data['kucoin_api_secret'])),
            'kucoin_api_key': encrypt_message(str(self.validated_data['kucoin_api_key'])),
            'kucoin_pass_pharese': encrypt_message(str(self.validated_data['kucoin_pass_pharese'])),
        }
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        if not attrs.get('username'):
            raise ValueError('username is required')
        if not attrs.get('password'):
            raise ValueError('password is required')
        if not attrs.get('kucoin_api_secret'):
            raise ValueError('kucoin_api_secret is required')
        if not attrs.get('kucoin_api_key'):
            raise ValueError('kucoin_api_key is required')
        if not attrs.get('kucoin_pass_pharese'):
            raise ValueError('kucoin_pass_pharese is required')

        return super().validate(attrs)



class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields used for authentication: username and password.
    It will try to authenticate the user with username/password when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},  # This will be used when the DRF browsable API is enabled
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
