from rest_framework.pagination import CursorPagination


class PostListPagination(CursorPagination):
    page_size = 10
    ordering = '-created_date'


class CommentListPagination(CursorPagination):
    page_size = 10
    ordering = '-created_date' 