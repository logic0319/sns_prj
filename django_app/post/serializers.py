from rest_framework import serializers

from post.models import Post, HashTag, Comment


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ('name',)




class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'author',
            'created_date',
            'modified_date',
            'like_users_counts',
            )


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content', 'modified_date')


class PostDetailSerializer(serializers.ModelSerializer):
    like_users_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    hashtags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'modified_date', 'view_count',
                  'like_users_count', 'hashtags', 'comments')

    def get_like_users_count(self,obj):
        return obj.like_users.count()


