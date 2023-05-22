from rest_framework import serializers
from . import models

UserForkucoin=models.UserForkucoin()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserForkucoin
        fields = ('username', 'password','api_name','api_key','api_secret','api_email')

    def create(self, validated_data):
        user = UserForkucoin.objects.create_user(**validated_data)
        return user

