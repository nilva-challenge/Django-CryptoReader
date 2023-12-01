from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'api_key', 'api_secret', 'api_passphrase',
                  'password', 'password_confirm')

        extra_kwargs = {
            'api_key': {'write_only': True},
            'api_secret': {'write_only': True},
            'api_passphrase': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return super().validate(attrs)

    def create(self, validated_data) -> User:
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)
