from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from post.functions import cal_distance
from post.models import Post, PostBookMark, PostLike
from post.serializers import PostCreateSerializer, PostDetailSerializer
from django.utils import timezone

__all__ = ('PostCreateView', 'PostDetailView', )


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        pk = request.user.pk
        request.data._mutable = True
        request.data['author'] = pk
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(hashtags=dict(self.request.data).get('hashtags'))


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs['pk']
        if not Post.objects.filter(pk=pk):
            return Response({"detail": "요청한 글이 존재하지 않습니다"}, status=status.HTTP_404_NOT_FOUND)
        else:
            instance = self.get_object()
            instance.view_counts += 1
            instance.save()

        if user.is_anonymous():
            Post.objects.filter(pk=pk).update(distance=None)
            return super().retrieve(request, *args, **kwargs)

        if user.is_authenticated():
            if PostBookMark.objects.filter(post=instance.pk, bookmark_user=request.user.pk):
                instance.is_bookmarked = True
                instance.save()
            else:
                instance.is_bookmarked = False
                instance.save()
            if PostLike.objects.filter(post=instance.pk, like_user=request.user.pk):
                instance.is_like = True
                instance.save()
            else:
                instance.is_like = False
                instance.save()

            if user.latitude is not None and user.hardness is not None:
                instance = self.get_object()
                author = instance.author
                stand = (user.latitude, user.hardness)
                sample = (author.latitude, author.hardness)
                dist = cal_distance(stand, sample)
                instance.distance = dist
                instance.save()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                instance = self.get_object()
                instance.distance = None
                instance.save()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().author.pk:
            request.data._mutable = True
            request.data['author'] = request.user.pk
            return super().update(request, *args, **kwargs)
        raise AuthenticationFailed(detail="수정 권한이 없습니다.")

    def perform_update(self, serializer):
        serializer.save(hashtags=dict(self.request.data).get('hashtags'))

    def destroy(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().author.pk:
            request.data._mutable = True
            request.data['author'] = request.user.pk
            return super().destroy(request, *args, **kwargs)
        raise AuthenticationFailed(detail="삭제 권한이 없습니다.") 