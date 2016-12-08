from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from member.models import CustomUser as User
from member.serializers import UserDetailSerializer

__all__ = ('UserUpdateView', )

class UserUpdateView(UpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        if request.user == self.get_object():
            return super().update(request, *args, **kwargs)
        return Response({"detail": "현재유저와 수정 요청된 유저가 다릅니다"}, status=status.HTTP_401_UNAUTHORIZED)
