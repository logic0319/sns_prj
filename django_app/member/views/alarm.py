from django.views.generic import DeleteView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

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
    serializer_class = AlarmListSerializer

    def perform_destroy(self, instance):
        if instance.post.author.pk != self.request.user.pk:
            raise AuthenticationFailed(detail="수정 권한이 없습니다.")
        instance.delete()