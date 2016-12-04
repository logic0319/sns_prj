from django.conf.urls import url
from .views import PostListView, PostDetailView, PostCreateView, CommentDetailView, \
    CommentCreateView

urlpatterns = [
    url(r'^list/$', PostListView.as_view(), name='post_list'),
    url(r'^add/$', PostCreateView.as_view(), name='post_create'),
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='post_detail'),
    url(r'^(?P<pk>\d+)/comment/$', CommentCreateView.as_view(), name='post_detail'),
]
