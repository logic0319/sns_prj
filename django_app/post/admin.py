from django.contrib import admin

from post.models import Alarm
from post.models import Post, Comment, HashTag, DefaultImg

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(HashTag)
admin.site.register(DefaultImg)
admin.site.register(Alarm)
