from django.contrib.auth import get_user_model
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
        return data
