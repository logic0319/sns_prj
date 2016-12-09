import binascii
import os

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from member.models import CustomUser as User
from member.serializers.passwordchange import PwChangeSerializer

__all__ = ('PasswordSendView', 'PasswordChangeView', )


class PasswordSendView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        if kwargs.get('email',''):
            email = kwargs['email']
            code = binascii.hexlify(os.urandom(12))[:12]
            if User.objects.filter(email=email):
                user = User.objects.get(email=email)
                user.set_password(code)
                user.save()
                send_mail(
                    '안녕하세요 parrot사이트의 id: {} 님의 임시비밀번호 입니다'.format(email),
                    'code: {}'.format(code),
                    'yunsoo3042@gmail.com',
                    [email],
                )
                return Response({"successs": "성공했습니다"},status=status.HTTP_200_OK)
            return Response({"detail": "입력하신 이메일은 존재하지 않는 유저입니다"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "get parameter로 email인자가 없습니다"}, status=status.HTTP_404_NOT_FOUND)


class PasswordChangeView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PwChangeSerializer
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return Response({"detail": "patch method는 허용되지 않습니다"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        print(request.data)
        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.do_update(serializer, request)
        print(serializer.data)
        return Response(serializer.data)

    def do_update(self, serializer, request):
        user = request.user
        password = request.data['password1']
        user.set_password(password)
        user.save()
        serializer.save()

