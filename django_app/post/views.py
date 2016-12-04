from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed

from post.models import Post, Comment
from post.serializers import PostListSerializer, PostDetailSerializer, CommentSerializer, PostCreateSerializer


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

    def perform_create(self, serializer):
        serializer.save(hashtags=dict(self.request.data).get('hashtags'))


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    def update(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().author.pk:
            request.data['author'] = request.user.pk
            return super().update(request, *args, **kwargs)
        raise AuthenticationFailed(detail="수정 권한이 없습니다.")

    def destroy(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().author.pk:
            request.data['author'] = request.user.pk
            return super().destroy(request, *args, **kwargs)
        raise AuthenticationFailed(detail="삭제 권한이 없습니다.")


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.pk
        request.data['post'] = kwargs.get('pk')
        return super().create(request, *args, **kwargs)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
