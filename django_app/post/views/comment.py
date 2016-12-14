from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from apis.fcm import *
from post.models import Comment, Post
from post.paginations import CommentListPagination
from post.serializers import CommentSerializer

__all__ = ('CommentListCreateView', 'CommentDetailView',)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CommentListPagination

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        post_pk = kwargs.get('post_pk')
        request.data['author'] = request.user.pk
        request.data['post'] = post_pk
        post = get_object_or_404(Post,pk=post_pk)
        registration_id = post.author.registration_id
        if registration_id:
            message_body = "누군가 내 글 '{}'...에 댓글을 달았습니다".format(post.content)
            messaging(message_body, post.pk, registration_id)
        return super().create(request, *args, **kwargs)


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
