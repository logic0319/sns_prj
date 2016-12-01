from django.conf.urls import url
from .views import PostListView

urlpatterns = [
    url(r'list/$', gPostListView.as_view(), name='rest_login'),
]
