from rest_framework import serializers
from post.models import Post

__all__ = ('PostListSerializer', )


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'content',
            'author',
            'created_date',
            'modified_date',
            'like_users_counts',
            'comments_counts',
            'distance',
            'img_thumbnail',
            )