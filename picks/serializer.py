from rest_framework import serializers

from .models import UserStock


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStock
        fields = ["user", "stock", "created_at"]
