from django.conf.urls import url
from .views import PostListView,PostDetailView,PostCreateView, MyPostListView,PostLikeView, PostBookMarkView

urlpatterns = [
    url(r'^$', PostListView.as_view(), name='post_list'),
    url(r'^my/$',MyPostListView.as_view(),name='my_post_list'),
    url(r'^add/$',PostCreateView.as_view(),name='post_create'),
    url(r'^(?P<pk>\d+)/$',PostDetailView.as_view(),name='post_detail'),
    url(r'^(?P<pk>\d+)/like/$',PostLikeView.as_view(),name='post_like'),
    url(r'^(?P<pk>\d+)/bookmark/$',PostBookMarkView.as_view(),name='post_bookmark'),
]
