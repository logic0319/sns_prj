from django.db import models
from member.models import CustomUser
from . import Post

__all__ = ('Comment', )


class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.CharField(max_length=255)
    author = models.ForeignKey(CustomUser)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
