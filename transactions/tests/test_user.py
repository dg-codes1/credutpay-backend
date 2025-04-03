
from rest_framework.test import APITestCase
from rest_framework import status
from transactions.models.user import User
from django.urls import reverse


class UserViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            wallet_balance=100.0,
        )

        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_user(self):
        """
        Test the creation of a new user using CreateUserView.
        """
        url = reverse("create-user")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_get_balance(self):
        """
        Test retrieving the wallet balance of the authenticated user.
        """
        url = reverse("users-get-balance", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["balance"], self.user.wallet_balance)

    def test_add_balance(self):
        """
        Test adding balance to the authenticated user's wallet.
        """
        url = reverse("users-add-balance", kwargs={"pk": self.user.pk})
        data = {"value": 50.0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.wallet_balance, 150.0)