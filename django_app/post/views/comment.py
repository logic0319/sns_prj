from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, APIException

from apis.fcm import *
from post.models import Alarm
from post.models import Comment, Post
from post.paginations import CommentListPagination
from post.serializers import CommentSerializer

__all__ = ('CommentListCreateView', 'CommentDetailView',)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CommentListPagination

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_pk'])

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        post_pk = kwargs.get('post_pk')
        request.data['author'] = request.user.pk
        request.data['post'] = post_pk
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()
        post = Post.objects.get(pk=self.kwargs.get('post_pk'))
        try:
            Alarm.objects.create(post=post, comment_author=self.request.user)
            post_pk = self.kwargs.get('post_pk')
            post = get_object_or_404(Post, pk=post_pk)
            registration_id = post.author.registration_id
            is_logined = Token.objects.filter(user=post.author)
            if registration_id and is_logined:
                message_body = "누군가 내 글 '{}'...에 댓글을 달았습니다".format(post.content)
                messaging(message_body, post.pk, registration_id)
        except Exception as e:
            raise APIException({"detail": e.args})


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_pk'])

    def perform_destroy(self, instance):
        if instance.author.pk != self.request.user.pk:
            raise AuthenticationFailed(detail="수정 권한이 없습니다.")
        instance.delete()

    def perform_update(self, serializer):
        if serializer.instance.author.pk != self.request.user.pk:
            raise AuthenticationFailed(detail="수정 권한이 없습니다.")
        serializer.save()
