from django.urls import path

from .swap_views import OneInchQuoteView, OneInchSwapTxView
from .views import MatchmakeView, RoomJoinView, RoomListCreateView

urlpatterns = [
    path("rooms/", RoomListCreateView.as_view(), name="rooms"),
    path("rooms/<uuid:room_id>/join/", RoomJoinView.as_view(), name="room-join"),
    path("matchmake/", MatchmakeView.as_view(), name="matchmake"),
    path("swap/1inch/quote/", OneInchQuoteView.as_view(), name="oneinch-quote"),
    path("swap/1inch/swap-tx/", OneInchSwapTxView.as_view(), name="oneinch-swap-tx"),
]

