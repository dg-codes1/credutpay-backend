from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from transactions.models import Transfer
from transactions.serializers import TransferSerializer


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payer = request.user
        receiver = serializer.validated_data['receiver']
        value = serializer.validated_data['value']

        if payer == receiver:
            return Response({'error': 'Transfers from the same user are not allowed'}, status=status.HTTP_400_BAD_REQUEST)

        if payer.wallet_balance < value:
            return Response({'error': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)

        payer.wallet_balance -= value
        receiver.wallet_balance += value

        Transfer.objects.create(payer=payer, receiver=receiver, value=value)

        payer.save()
        receiver.save()

        return Response({'message': 'Transfer was successful'}, status=status.HTTP_201_CREATED)
