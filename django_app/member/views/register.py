import hashlib

from django.http import HttpResponse
from django.views import View
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apis.mail import send_mail
from member.models import CustomUser
from member.serializers import TokenSerializer, RegisterSerializer
from sns_prj import settings

__all__ = ('RegisterView', 'EmailVerifyingView')


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )
    token_model = Token

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        content = request.META['HTTP_HOST'] + "/member/email_verify/" + user.get_email_verify_hash() + "/?email="+user.email
        send_mail("email verifying", content, (user.email,))
        Token.objects.get_or_create(user=user)

        return Response(TokenSerializer(user.auth_token).data, status=status.HTTP_200_OK)


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