from django.contrib.auth import (login as django_login,
                                 logout as django_logout)
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from member.serializers import RegisterSerializer, UserDetailSerializer
from .serializers import LoginSerializer,TokenSerializer


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = Token

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token,created = Token.objects.get_or_create(user=self.user)
        django_login(self.request,self.user)

    def get_response(self):
        serializer = TokenSerializer(instance=self.token, context={'request':self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request, *args, **kwargs):
        try:
            response = self.http_method_not_allowed(request,*args, **kwargs)
        except Exception as exc:
            response = self.handle_exception(exc)
        return self.finalize_response(request,response,*args,**kwargs)

    def post(self,request):
        return self.logout(request)

    def logout(self,request):
        request.user.auth_token.delete()
        django_logout(request)

        return Response({"success":_("Successfully logged out.")},
                        status=status.HTTP_200_OK)


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
