import uuid
from django.db import models
from .user import User


class Transfer(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_transfers"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_transfers"
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer from {self.payer.username} to {self.receiver.username}, value: {self.valor}"
