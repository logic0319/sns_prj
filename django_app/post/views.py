from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from post.models import Post
from post.serializers import PostListSerializer, PostDetailSerializer


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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


