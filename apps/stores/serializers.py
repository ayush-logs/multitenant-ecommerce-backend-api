from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.stores.models import Store


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["name", "description", "phone", "address"]


class StoreCreateSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "phone",
            "address",
            "owner",
            "created_at",
        ]
        read_only_fields = ["id", "owner", "created_at", "slug"]

