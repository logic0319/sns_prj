from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()

__all__ = ('CustomUserSerializer', )


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'age', 'gender')


