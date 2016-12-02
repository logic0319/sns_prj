from rest_framework import serializers

from post.models import Post, HashTag, Comment


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ('name',)


class PostListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    content = serializers.CharField(max_length=1000)
    like_user_count = serializers.SerializerMethodField()
    modified_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    author = serializers.CharField()

    def get_like_user_count(self, obj):
        return obj.like_users.count()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


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


