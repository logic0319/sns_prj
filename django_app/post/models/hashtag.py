
from django.db import models

__all__ = ('HashTag', )


class HashTag(models.Model):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name