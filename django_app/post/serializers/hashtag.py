from rest_framework import serializers
from post.models import HashTag
from post.models import Post

__all__ = ('HashTagSerializer', 'HashTag2Serializer', )


class HashTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = HashTag
        fields = ('name', )


class HashTag2Serializer(serializers.ModelSerializer):
    related_posts_counts = serializers.SerializerMethodField()

    class Meta:
        model = HashTag
        fields = ('name', 'related_posts_counts', )

    def get_related_posts_counts(self,obj):
        return Post.objects.filter(hashtags=obj).count()