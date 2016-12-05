from rest_framework import serializers
from post.models import Post, HashTag, PostLike, PostBookMark


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ('name',)


class PostListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField(max_length=1000)
    like_user_counts = serializers.SerializerMethodField()
    created_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    modified_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    author = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'content', 'author', 'modified_date', 'created_date', 'view_counts',
                  'like_users_counts','is_bookmarked')



class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'content', 'author', 'modified_date', 'created_date', 'view_counts',
                  'like_users_counts',)


class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLike
        fields = ('like_user','post')

class PostBookMarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostBookMark
        fields = ('bookmark_user','post')

