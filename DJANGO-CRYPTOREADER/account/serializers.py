from .utils.cryptography import encrypt_message, decrypt_message
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from .models import User


class RegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'kucoin_api_secret',
                  'kucoin_api_key', 'kucoin_pass_pharese')

    # def save(self):
    #     username = self.validated_data['username']
    #     password = encrypt_message(str(self.validated_data['password']))
    #     kucoin_api_secret = decrypt_message(
    #         self.validated_data['password'])
    #     return super().save(**self.validated_data)

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


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if not User.objects.filter(username=username):
            raise ValueError("you dont register with this user name")

        user = authenticate(username=username, password=password)
        if user:
            return user.tokens
