import uuid

from django.db import models


class Room(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        MATCHED = "matched", "Matched"
        CLOSED = "closed", "Closed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chain_id = models.PositiveIntegerField(default=80001)
    token_address = models.CharField(max_length=42)
    wager_amount = models.BigIntegerField(help_text="Token amount in smallest units (e.g., USDC=6 decimals)")

    player1_address = models.CharField(max_length=42)
    player2_address = models.CharField(max_length=42, blank=True, null=True)

    contract_address = models.CharField(max_length=42, blank=True, null=True)
    contract_game_id = models.BigIntegerField(blank=True, null=True)

    status = models.CharField(max_length=16, choices=Status.choices, default=Status.OPEN)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["status", "chain_id", "token_address", "wager_amount", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.id} ({self.status}) {self.wager_amount}"
