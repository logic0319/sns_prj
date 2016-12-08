from rest_framework import serializers
from post.models import HashTag

__all__ = ('HashTagSerializer', )


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ('name', )