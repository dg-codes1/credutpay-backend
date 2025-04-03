from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from transactions.models.user import User
from transactions.models.transfer import Transfer
from datetime import datetime, timedelta


class TransferViewTests(APITestCase):
    def setUp(self):
        self.payer = User.objects.create_user(
            username="payer",
            email="payer@example.com",
            password="testpassword",
            wallet_balance=200.0,
        )
        self.receiver = User.objects.create_user(
            username="receiver",
            email="receiver@example.com",
            password="testpassword",
            wallet_balance=50.0,
        )

        url = reverse("token_obtain_pair")
        data = {"username": "payer", "password": "testpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_transfer(self):
        """
        Test transfer between users
        """
        url = reverse("transactions-list")
        data = {
            "payer": self.payer.uuid,
            "receiver": self.receiver.uuid,
            "value": 100.0,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Transfer was successful")

        self.payer.refresh_from_db()
        self.receiver.refresh_from_db()
        self.assertEqual(self.payer.wallet_balance, 100.0)
        self.assertEqual(self.receiver.wallet_balance, 150.0)

        self.assertTrue(
            Transfer.objects.filter(payer=self.payer, receiver=self.receiver, value=100.0).exists()
        )

    def test_create_transfer_insufficient_balance(self):
        """
        Test attempt to trnasfer more than the payer's balance
        """
        url = reverse("transactions-list")
        data = {
            "payer": self.payer.uuid,
            "receiver": self.receiver.uuid,
            "value": 300.0,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Insufficient balance.")

    def test_list_transfers(self):
        """
        Test the listing of transfers made by the authenticated user.
        """
        Transfer.objects.create(payer=self.payer, receiver=self.receiver, value=50.0)
        Transfer.objects.create(payer=self.payer, receiver=self.receiver, value=30.0)

        url = reverse("transactions-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["value"], "30.00")
        self.assertEqual(response.data[1]["value"], "50.00")

    def test_list_transfers_with_date_filter(self):
        """
        Test transfers made within a specific date range.
        """
        Transfer.objects.create(
            payer=self.payer,
            receiver=self.receiver,
            value=30.0,
        )

        url = reverse("transactions-list")
        from_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
        to_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        response = self.client.get(f"{url}?from_date={from_date}&to_date={to_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 0)