import django_filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from post.models import Comment
from post.models import Post, PostLike, PostBookMark
from post.serializers import CommentSerializer
from post.serializers import PostListSerializer, PostDetailSerializer, PostLikeSerializer, PostCreateSerializer, PostBookMarkSerializer


class PostFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Post
        fields = ['hashtags__name', ]


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = PostFilter


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
        request.data._mutable = True
        request.data['author'] = pk
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(hashtags=dict(self.request.data).get('hashtags'))


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def update(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().author.pk:
            request.data['author'] = request.user.pk
            return super().update(request, *args, **kwargs)
        raise AuthenticationFailed(detail="수정 권한이 없습니다.")

    def perform_update(self, serializer):
        serializer.save(hashtags=dict(self.request.data).get('hashtags'))

    def destroy(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().author.pk:
            return super().destroy(request, *args, **kwargs)
        raise AuthenticationFailed(detail="삭제 권한이 없습니다.")


class PostLikeView(generics.CreateAPIView,
                   generics.DestroyAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        post = kwargs['pk']
        like_user = request.user.pk
        try:
            PostLike.objects.filter(post=post, like_user=like_user)
            return Response({"errors": "이미 좋아요를 누른 글입니다"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            pass
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
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostBookMarkView(generics.CreateAPIView,
                       generics.DestroyAPIView):
    queryset = PostBookMark.objects.all()
    serializer_class = PostBookMarkSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self,request,*args, **kwargs):
        post = kwargs['pk']
        user = request.user.pk
        try:
            PostBookMark.objects.get(post=post, bookmark_user=user)
            return Response({"errors": "이미 북마크한 글입니다"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            pass
        request.data._mutable = True
        request.data['bookmark_user'] = request.user.pk
        request.data['post'] = kwargs['pk']
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = request.user.pk
        try:
            instance = PostBookMark.objects.get(post=pk, bookmark_user=user)
        except:
            return Response({"errors": "아직 북마크하지 않은 글입니다"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.pk
        request.data['post'] = kwargs.get('pk')
        return super().create(request, *args, **kwargs)

