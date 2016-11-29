from rest_auth.app_settings import create_token, TokenSerializer
from rest_auth.models import TokenModel
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from member.serializer import RegisterSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )
    token_model = TokenModel

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user), status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        create_token(self.token_model, user, serializer)

        return user

    def get_response_data(self, user):
        return TokenSerializer(user.auth_token).data
