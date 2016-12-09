import random

from rest_framework import serializers

from post.models import DefaultImg
from post.models import Post, HashTag
from post.serializers import HashTagSerializer

__all__ = ('PostDetailSerializer', 'PostCreateSerializer', )


class PostDetailSerializer(serializers.ModelSerializer):
    hashtags = HashTagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'content', 'author', 'created_date', 'modified_date', 'view_counts',
                  'like_users_counts', 'distance','is_bookmarked', 'is_like','comments_counts', 'hashtags', 'img')

    def update(self, instance, validated_data):
        hashtags = self.initial_data.get('hashtags')
        post = instance

        post.content = validated_data.get('content', instance.content)
        post.img = validated_data.get('img', instance.img)

        post.save()

        if hashtags is not None:
            post.hashtags.all().delete()
            for hashtag in hashtags:
                h, created = HashTag.objects.get_or_create(name=hashtag)
                post.hashtags.add(h)
        return post


class PostCreateSerializer(serializers.ModelSerializer):
    hashtags = HashTagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'content', 'author', 'hashtags', 'img', 'img_thumbnail', 'created_date')

    def create(self, validated_data):
        hashtags = validated_data.pop('hashtags')

        if validated_data.get('img') is None and DefaultImg.objects.count() != 0:
                validated_data['img'] = DefaultImg.objects.all()[random.randrange(0, DefaultImg.objects.count())].img
        post = Post.objects.create(**validated_data)

        if hashtags is not None:
            for hashtag in hashtags:
                h, created = HashTag.objects.get_or_create(name=hashtag)
                post.hashtags.add(h)
        return post
