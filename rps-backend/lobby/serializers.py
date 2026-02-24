from rest_framework import serializers

from .models import Room


def _validate_evm_address(value: str) -> str:
    value = (value or "").strip()
    if not (value.startswith("0x") and len(value) == 42):
        raise serializers.ValidationError("Invalid EVM address")
    return value


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "id",
            "chain_id",
            "token_address",
            "wager_amount",
            "player1_address",
            "player2_address",
            "contract_address",
            "contract_game_id",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at", "player2_address"]

    def validate_token_address(self, value: str) -> str:
        return _validate_evm_address(value)

    def validate_player1_address(self, value: str) -> str:
        return _validate_evm_address(value)


class RoomJoinSerializer(serializers.Serializer):
    player2_address = serializers.CharField()

    def validate_player2_address(self, value: str) -> str:
        return _validate_evm_address(value)


class MatchmakeSerializer(serializers.Serializer):
    chain_id = serializers.IntegerField()
    token_address = serializers.CharField()
    wager_amount = serializers.IntegerField(min_value=1)
    player_address = serializers.CharField()

    def validate_token_address(self, value: str) -> str:
        return _validate_evm_address(value)

    def validate_player_address(self, value: str) -> str:
        return _validate_evm_address(value)

