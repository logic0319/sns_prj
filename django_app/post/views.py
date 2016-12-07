from django.shortcuts import get_object_or_404
import django_filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .paginations import PostListPagination, CommentListPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from post.models import Comment
from post.models import Post, PostLike, PostBookMark
from .functions import *
from django.contrib.auth import get_user_model
User = get_user_model()
from post.serializers import CommentSerializer
from post.serializers import PostListSerializer, PostDetailSerializer, PostLikeSerializer, PostCreateSerializer, \
    PostBookMarkSerializer


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
        Post.objects.all().update(distance=None)
        return Response({"errors": "사용자의 위치정보가 없습니다"}, status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        user = self.request.user
        user_dist = []
        stand = user.latitude, user.hardness
        for i in range(len(User.objects.exclude(pk=user.pk))):
            pk, pos_x, pos_y = User.objects.exclude(pk=user.pk)[i].position
            if User.objects.get(pk=pk).latitude is not None and User.objects.get(pk=pk).hardness is not None:
                dist = cal_distance(stand, (pos_x, pos_y))
                if dist <= 30:
                    user_dist.append((pk, dist))
        for pk, dis in user_dist:
            Post.objects.filter(author=pk).update(distance=dis)
        user_dist.sort(key=lambda x: x[1])
        near_user = [element[0] for element in user_dist]
        return Post.objects.filter(author__in=near_user)


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

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs['pk']
        if user.latitude is not None and user.hardness is not None:
            post = get_object_or_404(Post, pk=pk)
            author = post.author
            stand = (user.latitude, user.hardness)
            if author.latitude is not None and author.hardness is not None:
                sample = (author.latitude, author.hardness)
                dist = cal_distance(stand, sample)
            else:
                dist = None
            post.distance = dist
            instance = post
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            Post.objects.filter(pk=pk).update(distance=None)
            return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().author.pk:
            request.data._mutable = True
            request.data['author'] = request.user.pk
            return super().update(request, *args, **kwargs)
        raise AuthenticationFailed(detail="수정 권한이 없습니다.")

    def perform_update(self, serializer):
        serializer.save(hashtags=dict(self.request.data).get('hashtags'))

    def destroy(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().author.pk:
            request.data._mutable = True
            request.data['author'] = request.user.pk
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
        if PostLike.objects.filter(post=post, like_user=like_user):
            return Response({"errors": "이미 좋아요를 누른 글입니다"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        request.data._mutable = True
        request.data['like_user'] = request.user.pk
        request.data['post'] = kwargs['pk']
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = request.user.pk
        try:
            instance = PostLike.objects.get(post=pk, like_user=user)
        except PostLike.DoesNotExist:
            return Response({"errors": "아직 좋아요를 누르지 않은 글입니다"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostBookMarkView(generics.CreateAPIView,
                       generics.DestroyAPIView):
    queryset = PostBookMark.objects.all()
    serializer_class = PostBookMarkSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        post = kwargs['pk']
        user = request.user.pk
        try:
            PostBookMark.objects.get(post=post, bookmark_user=user)
            return Response({"errors": "이미 북마크한 글입니다"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except PostBookMark.DoesNotExist:
            request.data._mutable = True
            request.data['bookmark_user'] = request.user.pk
            request.data['post'] = kwargs['pk']
            return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = request.user.pk
        try:
            instance = PostBookMark.objects.get(post=pk, bookmark_user=user)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PostBookMark.DoesNotExist:
            return Response({"errors": "아직 북마크하지 않은 글입니다"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CommentListPagination

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['author'] = request.user.pk
        request.data['post'] = kwargs.get('post_pk')
        return super().create(request, *args, **kwargs)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_pk'])

    def perform_destroy(self, instance):
        if instance.author.pk != self.request.user.pk:
            raise AuthenticationFailed(detail="수정 권한이 없습니다.")
        instance.delete()

    def perform_update(self, serializer):
        if serializer.instance.author.pk != self.request.user.pk:
            raise AuthenticationFailed(detail="수정 권한이 없습니다.")
        serializer.save()
