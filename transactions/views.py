from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import User
from .serializers import UserSerializer, AddBalanceSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_balance(self, request, pk=None):
        user = self.get_object()
        return Response({'balance': user.wallet_balance}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_balance(self, request, pk=None):
        """
        Add the received value to the user wallet balance
        """
        user = self.get_object()
        serializer = AddBalanceSerializer(data=request.data)
        if serializer.is_valid():
            added_value = serializer.validated_data['value']
            user.wallet_balance += added_value
            user.save()
            return Response({'wallet_balance': user.wallet_balance}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
