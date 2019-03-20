from rest_framework import serializers

from post.models import Post

__all__ = ('PostListSerializer', )


class PostListSerializer(serializers.ModelSerializer):
    author_age = serializers.SerializerMethodField()
    author_gender = serializers.SerializerMethodField()

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
            'author_age',
            'author_gender',
            )

    def get_author_age(self, post):
        return post.author.age

    def get_author_gender(self, post):
        return post.author.gender
