from rest_framework import serializers
from post.models import Comment

__all__ = ('CommentSerializer', )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'content', 'author', 'created_date')