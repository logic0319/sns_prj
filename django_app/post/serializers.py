from rest_framework import serializers

from post.models import Comment
from post.models import Post, HashTag, PostLike, PostBookMark


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ('name',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'created_date')


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
            )


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    hashtags = HashTagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'content', 'author', 'created_date', 'modified_date', 'view_counts',
                  'like_users_counts', 'hashtags', 'comments','is_bookmarked')

    def update(self, instance, validated_data):
        hashtags = validated_data.pop('hashtags')
        post = Post.objects.get(pk=instance.pk)
        post.content = validated_data['content']
        post.save()
        post.hashtags.all().delete()

        if hashtags != None:
            for hashtag in hashtags:
                h, created = HashTag.objects.get_or_create(name=hashtag)
                post.hashtags.add(h)
        return post


class PostCreateSerializer(serializers.ModelSerializer):
    hashtags = HashTagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'content', 'author', 'hashtags', 'created_date')

    def create(self, validated_data):
        hashtags = validated_data.pop('hashtags')
        post = Post.objects.create(**validated_data)
        if hashtags != None:
            for hashtag in hashtags:
                h, created = HashTag.objects.get_or_create(name=hashtag)
                post.hashtags.add(h)
        return post


class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLike
        fields = ('like_user','post')


class PostBookMarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostBookMark
        fields = ('bookmark_user','post')

