from django.conf.urls import url
from .views import PostListView

urlpatterns = [
    url(r'list/$', PostListView.as_view(), name='rest_login'),
]
