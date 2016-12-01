from django.conf.urls import url
from .views import PostListView,PostDetailView

urlpatterns = [
    url(r'list/$', PostListView.as_view(), name='post_list'),
    url(r'detail/(?P<pk>\d+)/$',PostDetailView.as_view(),name='post_detail'),
]
