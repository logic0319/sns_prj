from django.db  import models
from . import Post
from member.models import CustomUser
__all__ = ('PostLike', 'PostBookMark', )


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    like_user = models.ForeignKey(CustomUser)
    created_date = models.DateTimeField(auto_now_add=True)


class PostBookMark(models.Model):
    post = models.ForeignKey(Post)
    bookmark_user = models.ForeignKey(CustomUser)
    created_date = models.DateTimeField(auto_now_add=True)