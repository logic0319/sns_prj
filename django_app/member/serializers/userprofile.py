from rest_framework import serializers
from django.contrib.auth import get_user_model

from post.models import Post, Comment, PostBookMark, PostLike

UserModel = get_user_model()

__all__ = ('UserProfileSerializer', )


class UserProfileSerializer(serializers.ModelSerializer):
    my_post_counts = serializers.SerializerMethodField()
    my_bookmark_counts = serializers.SerializerMethodField()
    received_like_counts = serializers.SerializerMethodField()
    my_post_commented_counts = serializers.SerializerMethodField()
    my_recent_posts = serializers.SerializerMethodField()
    my_bookmark_posts = serializers.SerializerMethodField()
    my_recent_comments = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ('email', 'gender', 'age', 'latitude', 'hardness', 'my_post_counts', 'my_bookmark_counts',
                  'received_like_counts', 'my_post_commented_counts', 'my_recent_posts', 'my_bookmark_posts',
                  'my_recent_comments', )


    def get_my_post_counts(self, obj):
        return Post.objects.filter(author=obj.pk).count()

    def get_my_bookmark_counts(self, obj):
        return PostBookMark.objects.filter(bookmark_user=obj.pk).count()

    def get_received_like_counts(self, obj):
        post_pk = Post.objects.filter(author=obj.pk).values_list('pk',flat=True)
        return PostLike.objects.filter(post__in=post_pk).count()

    def get_my_post_commented_counts(self, obj):
        post_pk = Post.objects.filter(author=obj.pk).values_list('pk', flat=True)
        return Comment.objects.filter(post__in=post_pk).count()

    def get_my_recent_posts(self, obj):
        return Post.objects.filter(author=obj.pk).order_by('-created_date')[:10].values_list('content','pk')

    def get_my_bookmark_posts(self, obj):
        bookmark_pk = PostBookMark.objects.filter(bookmark_user=obj.pk).order_by('-created_date')[:10].values_list('pk',flat=True)
        return Post.objects.filter(pk__in=bookmark_pk).values_list('content','pk')

    def get_my_recent_comments(self, obj):
        return Comment.objects.filter(author=obj.pk).order_by('-created_date')[:10].values_list('content','pk')