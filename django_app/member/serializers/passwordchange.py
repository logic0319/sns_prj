from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.core import exceptions
from rest_framework import serializers

UserModel = get_user_model()

__all__ = ('PwChangeSerializer', )


class PwChangeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        errors = dict()
        try:
            password_validation.validate_password(password=data['password1'], user=CustomUser)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return data
