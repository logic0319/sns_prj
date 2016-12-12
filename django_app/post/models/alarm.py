from django.db import models
from member.models import CustomUser
from . import Post

__all__ = ('Alarm', )


class Alarm(models.Model):
    post = models.ForeignKey(Post)
    comment_author = models.ForeignKey(CustomUser)

    @property
    def get_content(self):
        return self.post.content

