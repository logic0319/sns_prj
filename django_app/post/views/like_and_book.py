from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from apis.fcm import *

from post.models import PostBookMark, PostLike, Post
from post.serializers import PostBookMarkSerializer, PostLikeSerializer

__all__ = ('PostLikeView', 'PostBookMarkView',)


class PostLikeView(generics.CreateAPIView,
                   generics.DestroyAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        post_pk = kwargs['pk']
        like_user = request.user.pk
        if PostLike.objects.filter(post=post_pk, like_user=like_user):
            return Response({"detail": "이미 좋아요를 누른 글입니다"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        request.data._mutable = True
        request.data['like_user'] = request.user.pk
        request.data['post'] = post_pk
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()
        post_pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_pk)
        registration_id = post.author.registration_id
        is_logined = Token.objects.filter(user=post.author)
        if registration_id:
            message_body = "누군가 내 글 '{}'...에 좋아요를 눌렀습니다".format(post.content)
            messaging(message_body, post.pk, registration_id)

    def destroy(self, request, *args, **kwargs):
        post_pk = kwargs['pk']
        like_user = request.user.pk
        if PostLike.objects.filter(post=post_pk, like_user=like_user):
            instance = PostLike.objects.get(post=post_pk, like_user=like_user)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "아직 좋아요를 누르지 않은 글입니다"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostBookMarkView(generics.CreateAPIView,
                       generics.DestroyAPIView):
    queryset = PostBookMark.objects.all()
    serializer_class = PostBookMarkSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        post = kwargs['pk']
        bookmark_user = request.user.pk
        if PostBookMark.objects.filter(post=post, bookmark_user=bookmark_user):
            return Response({"detail": "이미 북마크한 글입니다"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        request.data._mutable = True
        request.data['bookmark_user'] = request.user.pk
        request.data['post'] = kwargs['pk']
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = kwargs['pk']
        bookmark_user = request.user.pk
        if PostBookMark.objects.filter(post=post, bookmark_user=bookmark_user):
            instance = PostBookMark.objects.get(post=post, bookmark_user=bookmark_user)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "아직 북마크하지 않은 글입니다"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

