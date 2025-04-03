from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from transactions.models import Transfer, User
from transactions.serializers import TransferSerializer, ListTransferenciaSerializer


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ListTransferenciaSerializer
        return TransferSerializer

    def get_queryset(self):
        if self.action in ['create', 'retrieve', 'list']:
            return User.objects.filter(pk=self.request.user.pk)
        return super().get_queryset()

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

    def list(self, request):
        user = request.user
        transfers = Transfer.objects.filter(payer=user).order_by('-date_time')

        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')

        if from_date and to_date:
            transfers = transfers.filter(
                date_time__date__range=[from_date, to_date])

        serializer = self.get_serializer(transfers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
