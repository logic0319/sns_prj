from django.conf.urls import url

from .views import PostListView, PostDetailView, PostCreateView, MyPostListView,PostLikeView, PostBookMarkView, \
    CommentListCreateView, CommentDetailView

urlpatterns = [
    url(r'^$', PostListView.as_view(), name='post_list'),
    url(r'^mylist/$', MyPostListView.as_view(), name='my_post_list'),
    url(r'^add/$', PostCreateView.as_view(), name='post_create'),
    url(r'^(?P<pk>\d+)/$', PostDetailView.as_view(), name='post_detail'),
    url(r'^(?P<post_pk>\d+)/comment/$', CommentListCreateView.as_view(), name='comment_list_create'),
    url(r'^(?P<post_pk>\d+)/comment/(?P<pk>\d+)/$', CommentDetailView.as_view(), name='comment_detail'),
    url(r'^(?P<pk>\d+)/like/$', PostLikeView.as_view(), name='post_like'),
    url(r'^(?P<pk>\d+)/bookmark/$', PostBookMarkView.as_view(), name='post_bookmark'),
]
