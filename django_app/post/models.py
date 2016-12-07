import os
from io import BytesIO

from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models

from member.models import CustomUser
from sns_prj.custom_storage import RandomFileName


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    view_counts = models.IntegerField(default=0)
    like_users = models.ManyToManyField(CustomUser, related_name='like_users_set', through='PostLike', blank=True)
    bookmark_users = models.ManyToManyField(CustomUser, related_name='bookmark_users_set',blank=True)
    hashtags = models.ManyToManyField('HashTag', blank=True)
    img = models.ImageField(upload_to=RandomFileName('photo/origin'), blank=True)
    img_thumbnail = models.ImageField(upload_to='photo/thumbnail', blank=True)

    def __str__(self):
        return "pk: {}, content: {}".format(self.pk, self.content)

    @property
    def like_users_counts(self):
        return self.like_users.count()

    @property
    def comments_counts(self):
        return self.comment_set.count()

    def is_bookmarked(self):
        return False

    def is_like(self):
        return False

    def make_thumbnail(self):

        size = (300, 300)

        f = default_storage.open(self.img.name)
        image = Image.open(f)
        ftype = image.format

        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        path, ext = os.path.splitext(self.img.name)
        name = os.path.basename(path)

        thumbnail_name = '%s_thumb%s' % (name, ext)

        temp_file = BytesIO()
        image.save(temp_file, ftype)
        temp_file.seek(0)

        content_file = ContentFile(temp_file.read())
        self.img_thumbnail.save(thumbnail_name, content_file)

        temp_file.close()
        content_file.close()
        f.close()

    def save(self, *args, **kwargs):
            image_changed = False

            if self.img and not self.img_thumbnail:
                image_changed = True

            if self.pk:
                ori = Post.objects.get(pk=self.pk)
                if ori.img != self.img:
                    image_changed = True

            super().save(*args, **kwargs)
            if image_changed:
                self.make_thumbnail()

    def delete(self, *args, **kwargs):
        if self.img.name.split("/")[1] != "default":
            default_storage.delete(self.img.name)
            default_storage.delete(self.img_thumbnail.name)
        super().delete(*args, **kwargs)


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


class DefaultImg(models.Model):
    img = models.ImageField(upload_to=RandomFileName('photo/default'))
