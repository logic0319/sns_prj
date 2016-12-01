from rest_framework import serializers

from post.models import Post, HashTag


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ('name',)


class PostListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    content = serializers.CharField(max_length=1000)
    like_user_count = serializers.SerializerMethodField()
    hashtags = HashTagSerializer(many=True, read_only=True)

    def get_like_user_count(self, obj):
        return obj.like_users.count()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'created_date', 'modified_date', 'view_count')
