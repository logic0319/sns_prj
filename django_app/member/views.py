from django.contrib.auth import (login as django_login,
                                 logout as django_logout)
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework import status, mixins
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import ugettext_lazy as _
from .serializers import LoginSerializer,TokenSerializer, UserDetailsSerializer


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
        print(request.user)
        try:
            print("로그아웃전 토큰{}".format(request.user.auth_token))
            request.user.auth_token.delete()
            print("로그아웃후 토큰{}".format(request.user.auth_token))
        except(AttributeError,ObjectDoesNotExist):
            print("123")
        django_logout(request)

        return Response({"success":_("Successfully logged out.")},
                        status=status.HTTP_200_OK)


class UserDetailsView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      GenericAPIView):

    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

