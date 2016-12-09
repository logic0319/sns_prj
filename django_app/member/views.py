import hashlib

from django.contrib.auth import (login as django_login,
                                 logout as django_logout)
from django.http import HttpResponse
from django.views import View
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.mail import send_mail
from member.serializers import RegisterSerializer
from sns_prj import settings
from .models import CustomUser as User, CustomUser
from .serializers import LoginSerializer,TokenSerializer
from .serializers import UserDetailSerializer


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = Token

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token,created = Token.objects.get_or_create(user=self.user)
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


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request, *args, **kwargs):
        try:
            response = self.http_method_not_allowed(request, *args, **kwargs)
        except Exception as exc:
            response = self.handle_exception(exc)
        return self.finalize_response(request, response, *args, **kwargs)

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        request.user.auth_token.delete()
        django_logout(request)

        return Response({"success": "Successfully logged out."},
                        status=status.HTTP_200_OK)


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )
    token_model = Token

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        content = request.META['HTTP_HOST'] + "/member/email_verify/" + user.get_email_verify_hash() + "/?email="+user.email
        send_mail("email verifying", content)
        Token.objects.get_or_create(user=user)

        return Response(TokenSerializer(user.auth_token).data, status=status.HTTP_200_OK)


class UserUpdateView(UpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        if request.user == self.get_object():
            return super().update(request, *args, **kwargs)
        return Response({"errors": "현재유저와 수정 요청된 유저가 다릅니다"}, status=status.HTTP_401_UNAUTHORIZED)


class EmailVerifyingView(View):

    def get(self, *args, **kwargs):
        email = self.request.GET['email']
        hash_input = email + settings.SALT
        m = hashlib.md5()
        m.update(hash_input.encode('utf-8'))
        hash_output = m.hexdigest()[0:10]

        if hash_output == kwargs['hash']:
            user = CustomUser.objects.get(email=email)
            user.is_active = True
            user.save()
            return HttpResponse("인증 성공")
        else:
            return HttpResponse("인증 실패")



