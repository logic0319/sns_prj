from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from member.serializers import TokenSerializer, RegisterSerializer

__all__ = ('RegisterView', )


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )
    token_model = Token

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Token.objects.get_or_create(user=user)

        return Response(TokenSerializer(user.auth_token).data, status=status.HTTP_200_OK)