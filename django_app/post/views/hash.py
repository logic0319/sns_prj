from rest_framework import generics

from post.models import HashTag
from post.serializers import HashTag2Serializer

__all__ = ('HashTagList', )


class HashTagList(generics.ListAPIView):
    queryset = HashTag.objects.all()
    serializer_class = HashTag2Serializer
