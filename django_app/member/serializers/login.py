from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework import serializers

UserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_email(self,email,password):
        user = None
        if email and password:
            user = authenticate(email=email, password=password)
        else:
            msg = ('email과 password 중 빈 값이 있습니다')
            raise exceptions.ValidationError(msg)
        return user

    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = None

        if email:
            try:
                user = self._validate_email(email,password)
            except UserModel.DoesNotExist:
                pass
        if not user:
            msg = _('유효하지 않은 로그인 정보 입니다.')
            raise exceptions.ValidationError(msg)
        attrs['user'] = user
        return attrs





