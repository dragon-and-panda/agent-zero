from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "chain_id", "wager_amount", "token_address", "player1_address", "player2_address")
    list_filter = ("status", "chain_id", "token_address")
    search_fields = ("id", "player1_address", "player2_address", "contract_address")
