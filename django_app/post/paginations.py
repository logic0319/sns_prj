from rest_framework.pagination import CursorPagination


class PostListPagination(CursorPagination):
    page_size = 10
    ordering = '-created_date'


class CommentListPagination(CursorPagination):
    page_size = 10
<<<<<<< HEAD
<<<<<<< HEAD
    ordering = '-created_date'
=======
    ordering = 'created_date'
>>>>>>> 817290eaff64a17b75608da235e8da03908e2d99
=======
    ordering = 'created_date'
>>>>>>> 2f20ef85efc680b28c6d23c961d2d9c83477a601
