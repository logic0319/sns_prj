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
        raise APIException({"errors": "수정 권한이 없습니다."},status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().author.pk:
            pk = request.user.pk
            request.data['author'] = pk
            return super().destroy(request, *args, **kwargs)
        raise APIException({"errors": "삭제 권한이 없습니다."},status=status.HTTP_401_UNAUTHORIZED)


class PostLikeView(generics.CreateAPIView,
                   generics.DestroyAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        post = kwargs['pk']
        like_user = request.user.pk
        if PostLike.objects.filter(post=post, like_user=like_user):
            return Response({"errors": "이미 좋아요를 누른 글입니다"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        request.data._mutable = True
        request.data['like_user'] = request.user.pk
        request.data['post'] = kwargs['pk']
        return super().create(request, *args,**kwargs)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = request.user.pk
        try:
            instance = PostLike.objects.get(post=pk,like_user=user)
        except:
            return Response({"errors":"아직 좋아요를 누르지 않은 글입니다"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_404_NOT_FOUND)
