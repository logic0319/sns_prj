from django.db import models
from sns_prj.custom_storage import RandomFileName

__all__ = ('DefaultImg', )


class DefaultImg(models.Model):
    img = models.ImageField(upload_to=RandomFileName('photo/default'))
