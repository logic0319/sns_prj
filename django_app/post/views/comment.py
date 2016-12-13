from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed

from post.models import Alarm, Post, Comment

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
        request.data['author'] = request.user.pk
        request.data['post'] = kwargs.get('post_pk')
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()
        post = Post.objects.get(pk=self.kwargs.get('post_pk'))
        Alarm.objects.create(post=post, comment_author=self.request.user)


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
