from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from member.models import CustomUser

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


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    gender = serializers.BooleanField(required=False)
    age = serializers.DateField(required=False)

    def create(self, validated_data):
        validated_data = {
            'email': validated_data.get('email', ''),
            'password': validated_data.get('password1', ''),
            'gender': validated_data.get('gender'),
            'age': validated_data.get('age'),
        }
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key',)