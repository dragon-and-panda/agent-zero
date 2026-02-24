from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import Room
from .serializers import RoomSerializer


class LobbyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("lobby", self.channel_name)
        await self.accept()

        rooms = await self._get_open_rooms()
        await self.send_json({"type": "rooms.snapshot", "rooms": rooms})

    async def disconnect(self, code):
        await self.channel_layer.group_discard("lobby", self.channel_name)

    async def receive_json(self, content, **kwargs):
        # reserved for future client->server messages
        if content.get("type") == "ping":
            await self.send_json({"type": "pong"})

    async def lobby_event(self, event):
        await self.send_json(event.get("event", {}))

    @database_sync_to_async
    def _get_open_rooms(self):
        qs = Room.objects.filter(status=Room.Status.OPEN).order_by("-created_at")[:100]
        return RoomSerializer(qs, many=True).data

