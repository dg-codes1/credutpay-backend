from rest_framework import serializers
from transactions.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("uuid", "username", "email", "wallet_balance", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class AddBalanceSerializer(serializers.Serializer):
    value = serializers.DecimalField(max_digits=10, decimal_places=2)
