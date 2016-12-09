from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()

__all__ = ('UserDetailSerializer', )


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('email', 'gender', 'age', 'latitude', 'hardness')
        read_only_fields = ('email',)