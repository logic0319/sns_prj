from django.contrib import admin
from post.models import Post, Comment, HashTag

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(HashTag)