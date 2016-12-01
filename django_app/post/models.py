from django.db import models
from member.models import CustomUser


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(CustomUser)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0)
    like_users = models.ManyToManyField(CustomUser, related_name='like_users_set')
    bookmark_users = models.ManyToManyField(CustomUser, related_name='bookmark_users_set')
    hashtags = models.ManyToManyField('HashTag')

    def __str__(self):
        return self.title


class HashTag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
