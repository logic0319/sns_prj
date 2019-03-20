from django.contrib.auth import login as django_login
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from member.serializers import LoginSerializer
from member.serializers import TokenSerializer

__all__ = ('LoginView', )


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = Token

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token, created = Token.objects.get_or_create(user=self.user)
        django_login(self.request, self.user)

    def get_response(self):
        serializer = TokenSerializer(instance=self.token, context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()
