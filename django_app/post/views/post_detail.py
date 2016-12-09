from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from post.functions import cal_distance
from post.models import Post, PostBookMark, PostLike
from post.serializers import PostCreateSerializer, PostDetailSerializer

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
        if user.is_anonymous():
            Post.objects.filter(pk=pk).update(distance=None)
            return super().retrieve(request, *args, **kwargs)
        if user.latitude is not None and user.hardness is not None:
            post = get_object_or_404(Post, pk=pk)
            author = post.author
            stand = (user.latitude, user.hardness)
            if author.latitude is not None and author.hardness is not None:
                sample = (author.latitude, author.hardness)
                dist = cal_distance(stand, sample)
            else:
                dist = None
            post.distance = dist
            instance = post
            if PostBookMark.objects.filter(post=instance.pk, bookmark_user=request.user.pk):
                instance.is_bookmarked = True
            else:
                instance.is_bookmarked = False
            if PostLike.objects.filter(post=instance.pk, like_user=request.user.pk):
                instance.is_like = True
            else:
                instance.is_like = False
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            Post.objects.filter(pk=pk).update(distance=None)
            instance = self.get_object()
            if PostBookMark.objects.filter(post=instance.pk, bookmark_user=request.user.pk):
                instance.is_bookmarked = True
            else:
                instance.is_bookmarked = False
            if PostLike.objects.filter(post=instance.pk, like_user=request.user.pk):
                instance.is_like = True
            else:
                instance.is_like = False
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

