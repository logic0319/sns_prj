import django_filters
from member.models import CustomUser as User
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from post.functions import cal_distance
from post.models import Post,PostBookMark
from post.paginations import PostListPagination
from post.serializers import PostListSerializer

__all__ = ('MyPostListView', 'PostListByDistanceView', 'PostListBookMarkedView', )


class PostFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Post
        fields = ['hashtags__name', ]


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = PostFilter
    pagination_class = PostListPagination


class MyPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)


class PostListByDistanceView(generics.ListAPIView):
    serializer_class = PostListSerializer
    pagination_class = PostListPagination
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.latitude is not None and user.hardness is not None:
            return self.list(request, *args, **kwargs)
        Post.objects.filter().update(distance=None)
        return Response({"detail": "사용자의 위치정보가 없습니다"}, status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        user = self.request.user
        user_dist = []
        stand = user.latitude, user.hardness
        users_except_me = User.objects.exclude(pk=user.pk)
        for i in range(len(users_except_me)):
            pk, pos_x, pos_y = users_except_me[i].position
            if User.objects.get(pk=pk).latitude is not None and User.objects.get(pk=pk).hardness is not None:
                dist = cal_distance(stand, (pos_x, pos_y))
                if dist <= 30:
                    user_dist.append((pk, dist))
        for pk, dis in user_dist:
            Post.objects.filter(author=pk).update(distance=dis)
        user_dist.sort(key=lambda x: x[1])
        near_user = [element[0] for element in user_dist]
        return Post.objects.filter(author__in=near_user)


class PostListBookMarkedView(generics.ListAPIView):
    serializer_class = PostListSerializer
    pagination_class = PostListPagination
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):

        return Post.objects.filter(pk__in=PostBookMark.objects.filter(
            bookmark_user=self.request.user).values_list('post', flat=True))



