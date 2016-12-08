from rest_framework import serializers
from post.models import PostLike, PostBookMark

__all__ = ('PostLikeSerializer', 'PostBookMarkSerializer', )


class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLike
        fields = ('like_user', 'post')


class PostBookMarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostBookMark
        fields = ('bookmark_user', 'post')