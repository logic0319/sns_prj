from django.contrib.auth import (login as django_login,
                                 logout as django_logout)
from django.core.exceptions import ObjectDoesNotExist
from rest_auth.app_settings import (create_token)
from rest_auth.models import TokenModel
from rest_framework import status, mixins
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import ugettext_lazy as _
from .serializers import LoginSerializer,TokenSerializer


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel

    def process_login(self):
        django_login(self.request, self.user)

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token = create_token(self.token_model,self.user,self.serializer)
        self.process_login()

    def get_response_serializer(self):
        response_serializer = TokenSerializer
        return response_serializer


    def get_response(self):
        serializer_class = self.get_response_serializer()
        user = self.serializer.validated_data['user']
        serializer = serializer_class(instance=self.token, context={'request':self.request})
        print(user.email)
        print(serializer.data)
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
        try:
            request.user.auth_token.delete()
        except(AttributeError,ObjectDoesNotExist):
            pass
        django_logout(request)

        return Response({"success":_("Successfully logged out.")},
                        status=status.HTTP_200_OK)



