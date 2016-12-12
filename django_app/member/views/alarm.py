from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from member.serializers.alarm import AlarmListSerializer
from post.models import Alarm, Post


class AlarmListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AlarmListSerializer

    def get_queryset(self):
        return Alarm.objects.filter(post__in=Post.objects.filter(author=self.request.user))


class AlarmDeleteView(DestroyAPIView):
    queryset = Alarm.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        if instance.post.author.pk != self.request.user.pk:
            raise AuthenticationFailed(detail="수정 권한이 없습니다.")
        instance.delete()


class AlarmPostDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = AlarmListSerializer

    def get_queryset(self):
        queryset = Alarm.objects.filter(post=self.kwargs['post_pk'])
        return queryset

    def delete(self):
        queryset = self.get_queryset()
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        if post.author.pk != self.request.user.pk:
            raise AuthenticationFailed(detail="수정 권한이 없습니다.")
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


