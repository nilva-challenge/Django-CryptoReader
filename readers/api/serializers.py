from rest_framework import serializers
from readers.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'account_id',
            'currency',
            'account_type',
            'balance',
            'available',
            'holds'
        ]