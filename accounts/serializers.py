from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.views import get_user_model
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    re_password = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = ['username','re_password','password','security_passphrase','kc_secret','kc_pp','kc_apikey']
        extra_kwargs = {
            'security_passphrase': {'write_only': True,'required':True},
            'kc_secret': {'write_only': True,'required':True},
            'kc_pp': {'write_only': True,'required':True},
            'kc_apikey': {'write_only': True,'required':True},
            'password': {'write_only': True,'required':True},
        }

    def validate(self, attrs) -> dict:
        """
        Checking if password and re_password are equal
        If not , raised a validation error
        :param attrs:
        :return:
        """
        if attrs.get('password') != attrs.get('re_password'):
            raise serializers.ValidationError({'Password':'Passwords does not match!'})
        del attrs['re_password']
        return super().validate(attrs)

    def save(self, **kwargs) -> User:
        """
        creates user with the validated data
        :param kwargs:
        :return:
        """
        return User.objects.create_user(**self.validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True,required=True)
    password = serializers.CharField(write_only=True,required=True)

    def validate(self, attrs) -> dict:
        """
        authenticating the user , if it returns a user , we generate and return access and refresh token
        if not , we raise an Authentication failed Error
        :param attrs:
        :return:
        """
        user = authenticate(username=attrs.get('username'), password=attrs.get('password'))
        if user:
            return user.tokens
        else:
            raise AuthenticationFailed('Invalid credentials!')

