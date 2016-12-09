from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import APIException

from member.models import CustomUser

UserModel = get_user_model()

__all__ = ('RegisterSerializer', )


class RegisterSerializer(serializers.Serializer):
    GENDER_CHOICE = (('M', "Male"), ('F', "Female"),)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICE, required=False)
    age = serializers.DateField(required=False)
    latitude = serializers.FloatField(required=False)
    hardness = serializers.FloatField(required=False)

    def create(self, validated_data):
        validated_data = {
            'email': validated_data.get('email', ''),
            'password': validated_data.get('password1', ''),
            'gender': validated_data.get('gender'),
            'age': validated_data.get('age'),
            'latitude': validated_data.get('latitude'),
            'hardness': validated_data.get('hardness'),
        }
        try:
            return CustomUser.objects.create_user(**validated_data)
        except Exception as e:
            raise APIException({"detail": e.args})

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data
