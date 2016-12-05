from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from post.models import Post, PostLike, PostBookMark
from post.serializers import PostListSerializer, PostDetailSerializer, PostLikeSerializer, PostCreateSerializer, PostBookMarkSerializer


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class MyPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        pk = request.user.pk
        request.data['author'] = pk
        return super().create(request, *args, **kwargs)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def update(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().author.pk:
            pk = request.user.pk
            request.data['author'] = pk
            return super().update(request, *args, **kwargs)
        raise APIException({"errors": "수정 권한이 없습니다."})

    def destroy(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().author.pk:
            pk = request.user.pk
            request.data['author'] = pk
            return super().destroy(request, *args, **kwargs)
        raise APIException({"errors": "삭제 권한이 없습니다."})


