from django.db import models

from member.models import CustomUser


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    view_counts = models.IntegerField(default=0)
    like_users = models.ManyToManyField(CustomUser, related_name='like_users_set', through='PostLike', blank=True)
    bookmark_users = models.ManyToManyField(CustomUser, related_name='bookmark_users_set',blank=True)
    hashtags = models.ManyToManyField('HashTag', blank=True)

    def __str__(self):
        return "pk: {}, content: {}".format(self.pk, self.content)

    @property
    def like_users_counts(self):
        return self.like_users.count()

    @property
    def comments_counts(self):
        return self.comment_set.count()

    @property
    def is_bookmarked(self):
        try:
            PostBookMark.objects.get(post=self)
            return True
        except PostBookMark.DoesNotExist:
            return False


class HashTag(models.Model):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.CharField(max_length=255)
    author = models.ForeignKey(CustomUser)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    like_user = models.ForeignKey(CustomUser)
    created_date = models.DateTimeField(auto_now_add=True)


class PostBookMark(models.Model):
    post = models.ForeignKey(Post)
    bookmark_user = models.ForeignKey(CustomUser)
    created_date = models.DateTimeField(auto_now_add=True)
