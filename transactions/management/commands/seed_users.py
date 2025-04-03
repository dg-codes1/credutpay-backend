from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from transactions.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User.objects.create(
            username="seeduser1",
            email="seeduser1@example.com",
            password=make_password("password1"),
        )

        User.objects.create(
            username="seeduser2",
            email="seeduser2@example.com",
            password=make_password("password2"),
        )

        self.stdout.write(self.style.SUCCESS("Seed users created"))
