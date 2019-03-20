import os
import uuid
#
# from django.conf import settings
from django.utils.deconstruct import deconstructible
# from storages.backends.s3boto3 import S3Boto3Storage
#
#
# class StaticStorage(S3Boto3Storage):
#     location = settings.STATICFILES_LOCATION
#
#
# class MediaStorage(S3Boto3Storage):
#     location = settings.MEDIAFILES_LOCATION
#
#
@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):
        # @note It's up to the validators to check if it's the correct file type in name or if one even exist.
        extension = os.path.splitext(filename)[1]
        return self.path % (uuid.uuid4(), extension)