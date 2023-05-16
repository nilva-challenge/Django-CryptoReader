from rest_framework import serializers
from readers.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'currency',
            'type',
            'balance',
            'available',
            'holds'
        ]