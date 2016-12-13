from rest_framework import serializers

from post.models import Alarm


class AlarmListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alarm
        fields = ('pk', 'post', 'comment_author', 'get_content')