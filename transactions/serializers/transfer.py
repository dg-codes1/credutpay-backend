from rest_framework import serializers
from transactions.models.transfer import Transfer


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = "__all__"

    def validate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError("Invalid value")
        return super().validate(value)


class ListTransferenciaSerializer(serializers.ModelSerializer):
    payer_username = serializers.CharField(
        source="payer.username", read_only=True)
    receiver_username = serializers.CharField(
        source="receiver.username", read_only=True
    )

    class Meta:
        model = Transfer
        fields = ("uuid", "payer_username",
                  "receiver_username", "value", "date_time")
