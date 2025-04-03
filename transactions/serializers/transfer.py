from rest_framework import serializers
from transactions.models import Transfer


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('payer', 'receiver', 'value')
