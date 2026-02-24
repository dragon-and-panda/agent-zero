from django.db import transaction
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Room
from .realtime import broadcast_lobby_event
from .serializers import MatchmakeSerializer, RoomJoinSerializer, RoomSerializer


class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all().order_by("-created_at")
    serializer_class = RoomSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        status_param = self.request.query_params.get("status", Room.Status.OPEN)
        chain_id = self.request.query_params.get("chainId")
        token = self.request.query_params.get("token")

        if status_param:
            qs = qs.filter(status=status_param)
        if chain_id:
            qs = qs.filter(chain_id=int(chain_id))
        if token:
            qs = qs.filter(token_address__iexact=token)
        return qs

    def perform_create(self, serializer):
        room = serializer.save(status=Room.Status.OPEN)
        broadcast_lobby_event({"type": "room.created", "room": RoomSerializer(room).data})


class RoomJoinView(APIView):
    def post(self, request, room_id):
        serializer = RoomJoinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            room = Room.objects.select_for_update().get(id=room_id)
            if room.status != Room.Status.OPEN:
                return Response({"detail": "Room is not open"}, status=status.HTTP_409_CONFLICT)
            if room.player1_address.lower() == serializer.validated_data["player2_address"].lower():
                return Response({"detail": "Cannot join your own room"}, status=status.HTTP_400_BAD_REQUEST)

            room.player2_address = serializer.validated_data["player2_address"]
            room.status = Room.Status.MATCHED
            room.updated_at = timezone.now()
            room.save(update_fields=["player2_address", "status", "updated_at"])

        data = RoomSerializer(room).data
        broadcast_lobby_event({"type": "room.matched", "room": data})
        return Response(data)


class MatchmakeView(APIView):
    """
    Match by wager (±10%) within same chain/token.
    If no match is found, create a new open room.
    """

    def post(self, request):
        serializer = MatchmakeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chain_id = serializer.validated_data["chain_id"]
        token_address = serializer.validated_data["token_address"]
        wager_amount = int(serializer.validated_data["wager_amount"])
        player_address = serializer.validated_data["player_address"]

        spread = wager_amount // 10
        min_wager = wager_amount - spread
        max_wager = wager_amount + spread

        with transaction.atomic():
            candidate = (
                Room.objects.select_for_update()
                .filter(
                    status=Room.Status.OPEN,
                    chain_id=chain_id,
                    token_address__iexact=token_address,
                    wager_amount__gte=min_wager,
                    wager_amount__lte=max_wager,
                )
                .exclude(player1_address__iexact=player_address)
                .order_by("created_at")
                .first()
            )

            if candidate:
                candidate.player2_address = player_address
                candidate.status = Room.Status.MATCHED
                candidate.updated_at = timezone.now()
                candidate.save(update_fields=["player2_address", "status", "updated_at"])
                room = candidate
                action = "matched"
            else:
                room = Room.objects.create(
                    chain_id=chain_id,
                    token_address=token_address,
                    wager_amount=wager_amount,
                    player1_address=player_address,
                    status=Room.Status.OPEN,
                )
                action = "created"

        room_data = RoomSerializer(room).data
        broadcast_lobby_event({"type": f"room.{action}", "room": room_data})
        return Response({"action": action, "room": room_data})

from django.shortcuts import render

# Create your views here.
