from rest_framework import generics
from post.models import HashTag
from post.serializers import HashTagSerializer, PostListSerializer

__all__ = ('HashTagList', )


class HashTagList(generics.ListAPIView):
    queryset = HashTag.objects.all()
    serializer_class = HashTagSerializer
