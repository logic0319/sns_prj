from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

UserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'passwrd'})


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
        if user:
            if not user.is_active:
                msg = _('User account is disabled')
                raise exceptions.ValidationError(msg)

        else:
            msg = _('Unable to log in with provided credentials')
            raise exceptions.ValidationError(msg)
        attrs['user'] = user
        return attrs



class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    user_email = serializers.SerializerMethodField()
    user_gender = serializers.SerializerMethodField()
    user_age = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = ('key','user','user_email','user_gender','user_age')

    def get_user_email(self,obj):
        return obj.user.email

    def get_user_gender(self,obj):
        return obj.user.gender

    def get_user_age(self,obj):
        return obj.user.age



class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        read_only_fields = ('email',)