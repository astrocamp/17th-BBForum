from rest_framework import serializers

from .models import FollowRelation


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRelation
        fields = ["follower", "following", "created_at"]
